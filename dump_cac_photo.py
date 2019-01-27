"""
    This program dumps general information about a CAC card.
"""
# Navtive
import logging
import optparse

# LL Smartcard
import llsmartcard.apdu as APDU
from llsmartcard.card import CAC
from PIL import Image
import getpass

def process_card(connection, options):
    """
        Will dump all of the interesting information from a CAC card to standard
        out
        
        WARNING: The PIN verify command will be sent multiple times.  If the 
        PIN is wrong, it will lock your CAC card!
    """

    # Open card
    card = CAC(connection)

    # Set this to your PIN.  Please be very careful with this!
    t_pin = getpass.getpass("PIN: ")
    PIN = list(bytearray(t_pin))
    
    # Do we have a PIN to access authenticated information?
    if PIN is not None:
        print("Printing NIST PIV Objects... (PIN PROTECTED)")
        data = card.read_object(APDU.APPLET.NIST_PIV,
                          APDU.OBJ_NIST_PIV.FACE,
                          pin=PIN)
        picture = data[0][1]
        with open("test.jp2", "w") as f:
            import re
            test = "".join([chr(int(x)) for x in re.findall(r"\d+", str(picture))])
            #import pdb; pdb.set_trace()
            found = test.find("\xFF\x4F\xFF\x51")
            if(not found): raise Exception("No JPEG 2000 photo!")
            f.write(test[found:])
        image = Image.open("test.jp2")
        image.save("test.jpeg", "JPEG")
        #import pdb; pdb.set_trace()
        print("Printing DoD CAC Objects... (PIN PROTECTED)")
        card.print_object(APDU.APPLET.DOD_CAC,
                          APDU.OBJ_DOD_CAC.CAC_PERSON,
                          pin=PIN)



if __name__ == "__main__":

    # Import our command line parser
    from llsmartcard import parser
    opts = optparse.OptionParser()

    # parse user arguments
    parser.command_line(opts, process_card)
