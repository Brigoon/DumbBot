import pickle
import herald

#load file, get all users in file, and get attributes of class before changes
heraldDict = pickle.load(open("herald/heraldUsers.p", "rb"))
users = list(heraldDict.keys())
old_attributes = list(heraldDict[users[0]].__dict__.keys())

#create object using new class and get attributes after changes
dummy_user = herald.HeraldUser('')
new_attributes = list(dummy_user.__dict__.keys())

#find intersection of class atributes from before and after changes
common_attributes = list(set(old_attributes) & set(new_attributes))
attributes_to_add = [i for i in new_attributes if i not in common_attributes]

if old_attributes.sort() != common_attributes.sort():
    raise NotImplementedError('The shared attributes between the former and new ' +
                              'HeraldUser classes do not match. Have any of the ' +
                              'former attributes changed names?')
else:
    #create new dictionary, copying old data and updating new data
    newHeraldDict = heraldDict.copy()
    for u in users:
        for a in attributes_to_add:
            #update user data using default value
            newHeraldDict[u].__setattr__(a, dummy_user.__getattribute__(a))
