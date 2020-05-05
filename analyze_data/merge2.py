from PIL import Image
import gc

#changables>>
# countriesOfInterest should contain only countries chosen from analyze6,7,8
countriesOfInterest = ['Azerbaijan','Georgia','Estonia','US','Italy','Bulgaria','Armenia','Germany']
#<<changables


#merge images
def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

for c in countriesOfInterest:
    img1=Image.open('../temp/an9/img9_cases_R_'+c+'.png')
    img2=Image.open('../temp/an10/img10_daily_'+c+'.png')

    get_concat_h(img1, img2).save('../img910_total_daily'+c+'.png')