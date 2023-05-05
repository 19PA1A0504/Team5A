from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from sklearn.model_selection import train_test_split
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import mysql.connector
import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score
import csv

# Create your views here.
from Client.forms import Userregister_Form
from Client.models import Userregister_Model, TweetModel, Feedback_Model
conn=mysql.connector.connect(host="localhost",database="women",user="root")

def user_login(request):
    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')
        try:
            enter = Userregister_Model.objects.get(name=name,password=password,status=0)
            request.session['name']=enter.id
            return redirect('user_mydetails')
        except:
            pass
    return render(request, 'client/user_login.html')

def user_register(request):
    if request.method == "POST":
        forms = Userregister_Form(request.POST)
        if forms.is_valid():
            forms.save()
            messages.success(request, 'You have been successfully registered')
            return redirect('user_login')
    else:
        forms = Userregister_Form()
    return render(request, 'client/user_register.html',{'form':forms})

def user_mydetails(request):
    name = request.session['name']
    ted = Userregister_Model.objects.get(id=name)
    return render(request, 'client/user_mydetails.html',{'object':ted})

def user_updatedetails(request):
    name = request.session['name']
    obj = Userregister_Model.objects.get(id=name)
    if request.method == "POST":
        UserName = request.POST.get('name', '')
        Email = request.POST.get('email', '')
        Password = request.POST.get('password', '')
        Phone_Number = request.POST.get('phoneno', '')
        Address = request.POST.get('address', '')
        Dob = request.POST.get('dob', '')
        country = request.POST.get('country', '')
        state = request.POST.get('state', '')
        city = request.POST.get('city', '')

        obj = get_object_or_404(Userregister_Model, id=name)
        obj.name = UserName
        obj.email = Email
        obj.password = Password
        obj.phoneno = Phone_Number
        obj.address = Address
        obj.dob = Dob
        obj.country = country
        obj.state = state
        obj.city = city
        obj.save(update_fields=["name", "email", "password", "phoneno", "address","dob","country","state","city"])
        return redirect('user_mydetails')


    return render(request, 'client/user_updatedetails.html',{'form':obj})

def tweet(request):
    name = request.session['name']
    status=0
    userObj = Userregister_Model.objects.get(id=name)
    result = ''
    pos = []
    neg = []
    oth = []
    se = 'se'
    if request.method == "POST":
        images = request.POST.get('images')
        twt = request.POST.get('tweet')

        if '#' in twt:
            startingpoint = twt.find('#')
            a = twt[startingpoint:]
            endingPoint = a.find(' ')
            title = a[0:endingPoint]
            result = title[1:]
        # return redirect('tweetpage')
        #svc=svm.SVC()
        dataset=pd.read_csv(r"C:\Users\laksh\Downloads\training.1600000.processed.noemoticon.csv",encoding='latin1')

        c=SVC(kernel='linear',random_state=0)
        #accuracy = accuracy_score(y_test,y_pred)*100
        lookup_dict={'rt':'retweet','dm': 'direct message','awsm': 'awesome','luv': 'love'}
        def _lookup_words(input_text):
            words=input_text.split()
            new_words=[]
            for word in words:
                if word.lower() in lookup_dict:
                    word=lookup_dict[word.lower()]
                #new_words.append(word) new_text=" ".join(new_words)
                return new_text
        for f in twt.split():
            if f in (
            'good', 'nice', 'better', 'miss', 'missed', 'new', 'best', 'excellent', 'safe','nice', 'work','better', 'happy', 'won',
            'win', 'awesome', 'love', 'positive', 'great','beautiful','encourage','active','care','clever','honest','polite','impressive','perfect','sincere','smart','unique','neat','pretty','fearless','kind','colorful','brave','unkind','behaviour'):
                pos.append(f)
            elif f in (
            'worst', 'not','unsafe','isnt','harrasment', 'jealous', 'suspended', 'nothing', 'pain', 'cant', 'waste', 'poor', 'error', 'imporve',
            'bad', 'sucked', 'sad', 'naked', 'worry', 'cheating','rape','cruel','careless','arrogant','aggressive','dishonest','greedy','harsh','rude','selfish','untrustworthy','fussy','overcritical','harmful','narrowminded','opposed','unpleasant','unkind','illmannered'):
                neg.append(f)
            else:
                oth.append(f)
        if len(pos) > len(neg):
            se = 'positive'
            status=0
        elif len(neg) > len(pos):
            se = 'negative'
            status=1
        else:
            se = 'nutral'
        TweetModel.objects.create(userId=userObj, tweet=twt, topics=result, sentiment=se,images=images,status=status )
    obj = TweetModel.objects.all()

    return render(request,'client/tweet.html',{'list_objects': obj,'result':result,'se':se})

def tweetview(request):
    obj = TweetModel.objects.all()

    return render(request,'client/tweetview.html',{'list_objects':obj})


def feedback(request):
    if request.method == "POST":
        name=request.POST.get('name')
        mobilenumber=request.POST.get('mobilenumber')
        feedback=request.POST.get('feedback')
        Feedback_Model.objects.create(name=name,mobilenumber=mobilenumber,feedback=feedback,)
        return redirect('feedback')

    return render(request,'client/feedback.html')
