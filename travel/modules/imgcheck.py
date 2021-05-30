import PIL.Image as Image

from nsfw import classify

def SFWCheck(image):
    sfw, nsfw = classify(image)
    if nsfw>0.5:
        return False
    else:
        return True

if __name__=="__main__":
    in_name = input("测试文件：")

    image = Image.open(in_name)
    sfw, nsfw = classify(image)

    print("SFW Probability: {}".format(sfw))
    print("NSFW Probability: {}".format(nsfw))
    if nsfw>0.5:
        print("NSFW!")
