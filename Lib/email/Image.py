# Copyright (C) 2001 Python Software Foundation
# Author: barry@zope.com (Barry Warsaw)

"""Class representing image/* type MIME documents.
"""

import imghdr

# Intrapackage imports
import MIMEBase
import Errors
import Encoders



class Image(MIMEBase.MIMEBase):
    """Class for generating image/* type MIME documents."""

    def __init__(self, _imagedata, _minor=None,
                 _encoder=Encoders.encode_base64, **_params):
        """Create an image/* type MIME document.

        _imagedata is a string containing the raw image data.  If this data
        can be decoded by the standard Python `imghdr' module, then the
        subtype will be automatically included in the Content-Type: header.
        Otherwise, you can specify the specific image subtype via the _minor
        parameter.

        _encoder is a function which will perform the actual encoding for
        transport of the image data.  It takes one argument, which is this
        Image instance.  It should use get_payload() and set_payload() to
        change the payload to the encoded form.  It should also add any
        Content-Transfer-Encoding: or other headers to the message as
        necessary.  The default encoding is Base64.

        Any additional keyword arguments are passed to the base class
        constructor, which turns them into parameters on the Content-Type:
        header.
        """
        if _minor is None:
            _minor = imghdr.what(None, _imagedata)
        if _minor is None:
            raise TypeError, 'Could not guess image _minor type'
        MIMEBase.MIMEBase.__init__(self, 'image', _minor, **_params)
        self.set_payload(_imagedata)
        _encoder(self)
