from .models import Tag, TagLocation

def checkIfTagInActive(tag, tags):
    pass

def print_tag_log(tag_ID):
    if Tag.objects.get(tagID=tag_ID):
        tag = Tag.objects.get(tagID=tag_ID)
        tag_vel = TagLocation.objects.filter(tagID=tag)
        for read in tag_vel:
            print("LOGGED ITEM:")
            print(read.tagID)
            print(read.timestamp)
            print(read.x_pos)
            print(read.y_pos)
            print(read.vx)
            print(read.vy)
        return 1
    else:
        return None
