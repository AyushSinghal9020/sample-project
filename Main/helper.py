import base64

def get_image_base64_str(image_path) : 
    '''
    Convert the image to base64 string

    Args :

        1) image_path : str : Path to the image

    Returns :
    
        1) str : Base64 string of the image
    '''

    return base64.b64encode(open(image_path , "rb").read()).decode('utf-8') 
