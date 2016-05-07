#!/usr/bin/env python
#
#
# VP21 RC
#
#
# Copyright 2016 Al Brown
#
# Epson Project Remote Control
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys

import serial.tools.list_ports
from wx import xrc
import wx


KEYCODES = {'buttonComputer': '43',
            'buttonVideo': '48',
            'buttonColour': '3f',
            'buttonMenu': '3c',
            'buttonMute': '3e',
            'buttonFreeze': '47',
            'buttonMinus': '29',
            'buttonPlus': '28',
            'buttonUp': '58',
            'buttonDown': '59',
            'buttonLeft': '5a',
            'buttonRight': '5b',
            'buttonEnter': '49',
            'buttonAuto': '4a',
            'buttonEsc': '3d'}


class FrameMain(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='VP21 RC',
                          style=wx.CAPTION |
                          wx.CLOSE_BOX |
                          wx.FRAME_TOOL_WINDOW)

        self._serial = None

        ui = self.__load_ui('main.xrc')
        ui.LoadPanel(self, 'Panel')

        self._status = wx.StatusBar(self, style=wx.STB_SHOW_TIPS)
        self.SetStatusBar(self._status)

        self._buttons = []
        cid = xrc.XRCID('buttonPower')
        self._buttons.append(cid)
        self.Bind(wx.EVT_BUTTON, self.__on_power, id=cid)

        for name, code in KEYCODES.iteritems():
            cid = xrc.XRCID(name)
            self._buttons.append(cid)
            self.Bind(wx.EVT_BUTTON,
                      lambda evt, code=code: self.__on_button(evt, code),
                      id=cid)

        ports = [port[0] for port in serial.tools.list_ports.comports()]
        choiceSerial = xrc.XRCCTRL(self, 'choiceSerial')
        choiceSerial.AppendItems(ports)
        if len(ports):
            choiceSerial.SetSelection(0)
            self.Bind(wx.EVT_CHOICE, self.__on_serial, choiceSerial)
            self.__open_serial()

        self.Fit()
        self.Show()

    def __on_power(self, _event):
        self._serial.write('PWR?\r\n')
        resp = self._serial.readall()
        if 'PWR=01' in resp:
            self._serial.write('PWR OFF\r\n')
        else:
            self._serial.write('PWR ON\r\n')

    def __on_button(self, _event, code):
        if self._serial is not None and self._serial.is_open:
            try:
                self._serial.write('KEY ' + code + '\r\n')
            except serial.SerialException as e:
                self._status.SetStatusText(e.message)

    def __on_serial(self, _event):
        self.__open_serial()

    def __open_serial(self):
        choiceSerial = xrc.XRCCTRL(self, 'choiceSerial')
        port = choiceSerial.GetStringSelection()
        if self._serial is not None:
            try:
                self._serial.close()
            except serial.SerialException:
                pass

        self.__buttons_enable(False)

        try:
            self._serial = serial.Serial(port,
                                         9600,
                                         timeout=0.5,
                                         write_timeout=0)
            self._serial.reset_input_buffer()
            self._serial.reset_output_buffer()
        except serial.SerialException as e:
            self._status.SetStatusText(e.message)
            return

        self.__buttons_enable(True)
        self._status.SetStatusText('Connected')

    def __buttons_enable(self, enable):
        for cid in self._buttons:
            self.FindWindowById(cid).Enable(enable)

    def __get_ui_dir(self):
        if getattr(sys, 'frozen', False):
            resDir = os.path.join(sys._MEIPASS, 'ui')
        else:
            scriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))
            resDir = os.path.join(scriptDir, 'gui', 'ui')

        return resDir

    def __load_ui(self, filename):
        path = os.path.join(self.__get_ui_dir(), filename)
        return xrc.XmlResource(path)
