from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SuperTrait, Speaker, Trait, Conversation, Line, LinePiece, EvaluationFunction
import json, re

def index(request):
    return main(request)

def main(request):
    data={}
    conversations=Conversation.objects.all()
    data['conversations']=conversations
    return render(request, 'chat/main.html', data)

def chat(request, conversation=1):
    data={}
    speaker1=Speaker.objects.get(pk=1)
    speaker2=Speaker.objects.get(pk=2)
    speaker1.cpu=False
    speaker2.cpu=True
    data['speaker1']=speaker1
    data['speaker2']=speaker2
    conversation=Conversation.objects.get(pk=conversation)
    data['conversation']=conversation
    return render(request, 'chat/chat.html',data)

def answer(request):
    message=request.GET.get("message")
    line=request.GET.get("line")
    if not message:
        speaker=request.GET.get("speaker")
        speaker=Speaker.objects.get(pk=speaker)
        lines=request.GET.get("lines")
        lines=json.loads(lines)
        lines=Line.objects.filter(pk__in=lines)
        answer=speaker.chooseLine(lines)
        message=speaker.speak(answer)
    else:
        answer=Line.objects.get(pk=line)
    data={
        'message':message,
        'line':answer
    }
    return render(request, 'chat/bubble.html',data)

def choices(request):
    speaker=request.GET.get("speaker")
    speaker=Speaker.objects.get(pk=speaker)
    lines=request.GET.get("lines")
    lines=json.loads(lines)
    lines=Line.objects.filter(pk__in=lines)
    data={'lines':[]}
    for line in lines:
        message=speaker.speak(line)
        data['lines'].append({
            'message':message,
            'line':line
        })
    return render(request, 'chat/choices.html',data)

def editor(request):
    conversation=Conversation.objects.get(pk=2)
    data={'conversation':conversation}
    return render(request, 'chat/editor.html',data)

@csrf_exempt
def speaker(request,pk=None):
    data={}
    speaker=None
    if pk not in [1,2]:
        return HttpResponse()
    if pk:
        try:
            speaker=Speaker.objects.get(pk=pk)
            data['speaker']=speaker
        except:
            pass
    if request.method=='GET':
        traits=SuperTrait.objects.all()
        data['traits']=traits

        return render(request, 'chat/speaker.html',data)
    elif request.method=='POST':
        speakerdata=json.loads(request.POST.get('speaker'))
        name=speakerdata['name']
        if not speaker:
            speaker=Speaker(
            )
        speaker.name=name
        speaker.save()
        for trait in speakerdata['traits']:
            try:
                supertrait=SuperTrait.objects.get(pk=trait)
                try:
                    trait_ = Trait.objects.get(
                        type=supertrait,
                        speaker=speaker
                    )
                except:
                    trait_ = Trait(
                        type=supertrait,
                        speaker=speaker
                    )
                    trait_.save()
                trait_.value=speakerdata['traits'][trait]
                trait_.save()
            except Exception as e:
                pass

        print (speakerdata)
        return HttpResponse(name)
