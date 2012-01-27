# -*- coding: utf-8 -*-
# Author: Milan Nikolic <gen2brain@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import QtGui

DocType = 0
Entity = 1
Tag = 2
Comment = 3
AttributeName = 4
AttributeValue = 5

State_Text = -1
State_DocType = 0
State_Comment = 1
State_TagStart = 2
State_TagName = 3
State_InsideTag = 4
State_AttributeName =5
State_SingleQuote = 6
State_DoubleQuote = 7
State_AttributeValue = 8

class Highlighter(QtGui.QSyntaxHighlighter):

    def __init__(self, parent=None):
        QtGui.QSyntaxHighlighter.__init__(self, parent)
        self.m_colors = {}
        self.m_colors[DocType] = QtGui.QColor(192, 192, 192)
        self.m_colors[Entity] = QtGui.QColor(128, 128, 128)
        self.m_colors[Tag] = QtGui.QColor(136, 18, 128)
        self.m_colors[Comment] = QtGui.QColor(35, 110, 37)
        self.m_colors[AttributeName] = QtGui.QColor(153, 69, 0)
        self.m_colors[AttributeValue] = QtGui.QColor(36, 36, 170)

    def highlightBlock(self, text):
        state = int(self.previousBlockState())
        length = text.length()
        start = 0
        pos = 0

        while (pos < length):

            if state == State_Text:
                while (pos < length):
                    ch = text.at(pos)
                    if ch.toAscii() == '<':
                        if text.mid(pos, 4).toAscii() == "<!--":
                            state = State_Comment
                        else:
                            if text.mid(pos, 9).toUpper() == "<!DOCTYPE":
                                state = State_DocType
                            else:
                                state = State_TagStart
                        break
                    elif ch.toAscii() == "&":
                        start = pos
                        while pos < length:
                            if text.at(pos + 1).toAscii() != ";":
                                self.setFormat(start, pos - start, self.m_colors[Entity])
                    else:
                        pos += 1

            elif state == State_Comment:
                start = pos
                while pos < length:
                    if text.mid(pos, 3).toAscii() == "-->":
                        pos += 3
                        state = State_Text
                        break
                    else:
                        pos += 1
                self.setFormat(start, pos - start, self.m_colors[Comment])

            elif state == State_DocType:
                start = pos
                while pos < length:
                    ch = text.at(pos)
                    pos += 1
                    if ch.toAscii() == ">":
                        state = State_Text
                        break
                self.setFormat(start, pos - start, self.m_colors[DocType])

            # at '<' in e.g. "<span>foo</span>"
            elif state == State_TagStart:
                start = pos + 1
                while pos < length:
                    ch = text.at(pos)
                    pos += 1
                    if ch.toAscii() == ">":
                        state = State_Text
                        break
                    if not ch.isSpace():
                        pos -= 1
                        state = State_TagName
                        break

            # at 'b' in e.g "<blockquote>foo</blockquote>"
            elif state == State_TagName:
                start = pos
                while pos < length:
                    ch = text.at(pos)
                    pos += 1
                    if ch.isSpace():
                        pos -= 1
                        state = State_InsideTag
                        break
                    if ch.toAscii() == ">":
                        state = State_Text
                        break
                self.setFormat(start, pos - start, self.m_colors[Tag])

            # anywhere after tag name and before tag closing ('>')
            elif state == State_InsideTag:
                start = pos
                while pos < length:
                    ch = text.at(pos)
                    pos += 1
                    if ch.toAscii() == "/":
                        continue
                    if ch.toAscii() == ">":
                        state = State_Text
                        break
                    if not ch.isSpace():
                        pos -= 1
                        state = State_AttributeName
                        break

            # at 's' in e.g. <img src=bla.png/>
            elif state == State_AttributeName:
                start = pos
                while pos < length:
                    ch = text.at(pos)
                    pos += 1
                    if ch.toAscii() == "=":
                        state = State_AttributeValue
                        break
                    if ch.toAscii() == ">" or ch.toAscii() == "/":
                        state = State_InsideTag
                        break
                self.setFormat(start, pos - start, self.m_colors[AttributeName])

            # after '=' in e.g. <img src=bla.png/>
            elif state ==State_AttributeValue:
                # find first non-space character
                start = pos
                while pos < length:
                    ch = text.at(pos)
                    pos += 1
                    if ch.toAscii() == "'":
                        state = State_SingleQuote
                        break
                    if ch.toAscii() == '"':
                        state = State_DoubleQuote
                        break
                    if not ch.isSpace():
                        break

                if state == State_AttributeValue:
                    # attribute value without quote
                    # just stop at non-space or tag delimiter
                    start = pos
                    while pos < length:
                        ch = text.at(pos)
                        if ch.isSpace():
                            break
                        if ch.toAscii() == ">" or ch.toAscii() == "/":
                            break
                        pos += 1
                    state = State_InsideTag
                    self.setFormat(start, pos - start, self.m_colors[AttributeValue])

            # after the opening single quote in an attribute value
            elif state == State_SingleQuote:
                start = pos
                while pos < length:
                    ch = text.at(pos)
                    pos += 1
                    if ch.toAscii() == "'":
                        break
                state = State_InsideTag
                self.setFormat(start, pos - start, self.m_colors[AttributeValue])

            # after the opening double quote in an attribute value
            elif state == State_DoubleQuote:
                start = pos
                while pos < length:
                    ch = text.at(pos)
                    pos += 1
                    if ch.toAscii() == '"':
                        break
                state = State_InsideTag
                self.setFormat(start, pos - start, self.m_colors[AttributeValue])
            else:
                while (pos < length):
                    ch = text.at(pos)
                    if ch.toAscii() == '<':
                        if text.mid(pos, 4) == "<!--":
                            state = State_Comment
                        else:
                            if text.mid(pos, 9).toUpper() == "<!DOCTYPE":
                                state = State_DocType
                            else:
                                state = State_TagStart
                        break
                    elif ch.toAscii() == "&":
                        start = pos
                        while pos < length:
                            if text.at(pos + 1) != ";":
                                self.setFormat(start, pos - start, self.m_colors[Entity])
                    else:
                        pos += 1

        self.setCurrentBlockState(state)
