import time

import streamlit as st
import torch
from torch.autograd import Variable
from torchvision.transforms import ToTensor, ToPILImage

from model import Generator


def test_single_image(lr_image, upscale_factor, epoch_num):
    test_mode = False
    model_name = 'netG_epoch_{}_{}.pth'.format(upscale_factor, epoch_num)

    st.write('**The low-res image**')
    st.image(lr_image, use_column_width=True)
    
    model = Generator(upscale_factor).eval()
    if test_mode:
        model.cuda()
        model.load_state_dict(torch.load('epochs/' + model_name))
    else:
        model.load_state_dict(torch.load('epochs/' + model_name, map_location=lambda storage, loc: storage))
    # volatile is no longer available
    # image = Variable(ToTensor()(lr_image), volatile=True).unsqueeze(0)
    with torch.no_grad():
        image = Variable(ToTensor()(lr_image)).unsqueeze(0)
    if test_mode:
        image = image.cuda()

    start = time.clock()
    out = model(image)
    elapsed = (time.clock() - start)
    print('Process time: ' + str(elapsed) + 's')
    out_img = ToPILImage()(out[0].data.cpu())
    st.write('**The super-res image (sacled at {}x)**'.format(upscale_factor))
    st.image(out_img, use_column_width=True)
