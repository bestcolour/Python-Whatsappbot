class something():
    def __init__(self,name):
        self.name = name
        pass


mylist = [something("hi"),something("b")]
instance = something("die") 
mylist.append(instance)

print(mylist)

mylist.remove(instance)

print(mylist)

