# Copyright (C) 2001-2006 Python Software Foundation
# Author: Barry Warsaw
# Contact: email-sig@python.org

"""Class representing text/* type MIME documents."""

__all__ = ['MIMEText']

from email.encoders import encode_7or8bit
from email.mime.nonmultipart import MIMENonMultipart



class MIMEText(MIMENonMultipart):
    """Class for generating text/* type MIME documents."""

    def __init__(self, _text, _subtype='plain', _charset='us-ascii'):
        """Create a text/* type MIME document.

        _text is the string for this message object.

        _subtype is the MIME sub content type, defaulting to "plain".

        _charset is the character set parameter added to the Content-Type
        header.  This defaults to "us-ascii".  Note that as a side-effect, the
        Content-Transfer-Encoding header will also be set.
        """
        MIMENonMultipart.__init__(self, 'text', _subtype,
                                  **{'charset': _charset})

        # If _charset was defualted, check to see see if there are non-ascii
        # characters present. Default to utf-8 if there are.
        # XXX: This can be removed once #7304 is fixed.
        if _charset =='us-ascii':
            try:
                _text.encode(_charset)
            except UnicodeEncodeError:
                _charset = 'utf-8'

        self.set_payload(_text, _charset)
