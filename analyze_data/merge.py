from PIL import Image
import gc

#changables>>
# countriesOfInterest should contain only countries chosen from analyze6,7,8
countriesOfInterest = ['Azerbaijan', 'Georgia', 'Armenia', 'Turkey', 'Estonia', 'Latvia', 'Lithuania', 'US', 'Germany','Italy','Spain', 'United Kingdom', 'Russia','Portugal','Poland']
mergeOptions = ['an6/cases','an7/deaths','an8/recov']
numberOfRows = 3
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

for opt in mergeOptions:
    #read images and store in imgs = []
    imgs = []
    for i in range(len(countriesOfInterest)):
        img = Image.open("../temp/"+opt+"_"+countriesOfInterest[i]+".png")
        imgs.append(img)

    #build rows
    j=0
    imgs_v = [0] * numberOfRows
    for i in range(len(countriesOfInterest)):
        if (j >= numberOfRows): j=0
        if (i < numberOfRows): imgs_v[i] = imgs[i] #initialize array
        else : imgs_v[j]=(get_concat_h(imgs_v[j],imgs[i])) #concatenate images to initialized arra
        j=j+1

    #build image
    for i in range(1, numberOfRows):
        imgs_v[0] = get_concat_v(imgs_v[0],imgs_v[i]) #concatenate rows to each other

    imgs_v[0].save('../img678_daily_'+opt[4:]+'_Merged.png')