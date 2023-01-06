from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        error = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        special_symbols = ['$','@','#','%','^','&']
        if len(postData['first_name']) < 3 :
            error['first_name'] = "first name should be at least 3 characters"
        if len(postData['last_name']) < 3 :
            error['last_name'] = "last name should be at least 3 characters"
        if not email_regex.match(postData['email']) :
            error['email'] = "invaild email"
        if len(postData['password']) < 8:
            error['password_less_than'] = "Password must have atleast 6 characters"
        if len(postData['password']) > 20 :
            error['password_grather_than'] = "'Password cannot have more than 20 characters"
        if not any(characters.isupper() for characters in postData['password']):
            error['password_notInclude_upper'] = "Password must have at least one uppercase character"
        if not any(characters.islower() for characters in postData['password']):
            error['password_notInclude_lower'] = "Password must have at least one lowercase character"
        if not any(characters.isdigit() for characters in postData['password']):
            error['password_notInclude_number'] = "Password must have at least one numeric character."
        if not any(characters in special_symbols for characters in postData['password']):
            error['password_symbol'] = "Password should have at least one of the symbols $@#%^&"
        if postData['password'] != postData['confirm_password'] :
            error['not_the_same'] = "please insert password as the same"
        return error

    def sigin_validator(self, postData):
        error = {}
        userid = User.objects.filter(email = postData['email'])
        print(postData['email'])
        if len(userid) == 0 :
            error['user_not_found'] = "user not exisit"
            return error
        user = userid[0]
        if (bcrypt.checkpw(postData['password'].encode(), user.password.encode()) != True):
            error['incorrect_password'] = "you insert password error"
        return error

    def pypie_validator(self, postData):
        error = {}
        if len(postData['name']) <3:
            error['name'] = "pypie name should be at least 3 characyers"
        if len(postData['filling']) <3:
            error['filling'] = "pypie filling should be at least 3 characyers"
        if len(postData['crust']) <3:
            error['crust'] = "pypie crust should be at least 3 characyers"
        return error
# user table
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    # pypies = list of pypies which made by user
    objects = UserManager()

# pypie table
class Pypie(models.Model):
    name = models.CharField(max_length=255)
    filling = models.CharField(max_length=255)
    crust = models.CharField(max_length=255)
    user = models.ForeignKey(User , related_name="pypies" , on_delete=models.DO_NOTHING)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

# vote table
class Votes(models.Model):
    vote = models.IntegerField()
    user = models.ForeignKey(User , related_name="votes" , on_delete=models.DO_NOTHING)
    pypie = models.ForeignKey(Pypie , related_name="votes" , on_delete=models.DO_NOTHING)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


# add vote
def vote_on(vote,userId,pypieId):
    user = User.objects.get(id = userId)
    pypie = Pypie.objects.get(id = pypieId)
    return Votes.objects.create(vote = vote , user = user , pypie = pypie)

# get vote num of pypie
def get_vote(pypieId):
    pypie = Pypie.objects.get(id = pypieId)
    print("sum = ",pypie.votes.sum())
    return pypie.votes.sum()

# register new user
def Register(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 
    if (request.POST['confirm_password'] == password):
        return User.objects.create(first_name = first_name , last_name = last_name, email = email , password = pw_hash )

# login current user
def Login(request):
    user = User.objects.filter(email = request.POST['email'])
    if user:
        loged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), loged_user.password.encode()):
            # request.session['userid'] = loged_user.id
            return loged_user.id
    else:
        return None

# add pypie
def add_Pypie(name , filling , crust , userId):
    print("3333")
    return Pypie.objects.create(name = name , filling = filling , crust = crust , user = userId)
    
# get pypie of user
def get_pypie(user):
    return user.pypies.all()

# get spacial pypie
def get_one_pypie(pypieId):
    pypie = Pypie.objects.get(id = pypieId)
    return pypie

# get all pypie in database
def get_all_pypie(request):
    return Pypie.objects.all()

# edit pypie data
def edit_pypie(pypie,name,filling,crust):
    pypie.name = name
    pypie.filling = filling
    pypie.crust = crust
    return pypie.save()

# delete pypie
def del_pypie(pypieId):
    pypie = Pypie.objects.get(id = pypieId)
    return pypie.delete()

