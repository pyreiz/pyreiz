import os 
LIBPATH = os.path.dirname(os.path.realpath(__file__)).split(os.path.sep +
                                                            'experiment')[0]
MEDIAPATH = os.path.join(LIBPATH, 'media')
AUDIOPATH = os.path.join(MEDIAPATH, 'wav')
IMGPATH = os.path.join(MEDIAPATH, 'img')
                                                            
del os
