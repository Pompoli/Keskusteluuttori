from django.db import models
from random import randint
import re


class NonStrippingTextField(models.TextField):
    """A TextField that does not strip whitespace at the beginning/end of
    it's value.  Might be important for markup/code."""

    def formfield(self, **kwargs):
        kwargs['strip'] = False
        return super(NonStrippingTextField, self).formfield(**kwargs)

class RememberDates(models.Model):
    insert_date=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Evaluetable(RememberDates):
    HARD_MIN=1
    SOFT_MIN=5
    START_VALUE=20
    def evaluate(self, speaker):
        p=self.START_VALUE
        for f in self.functions.all():
            p+=f.evaluate(speaker.traits)
        try:
            chaos=speaker.traits.get(type_id=8).value
        except:
            chaos=0
        minimum = self.SOFT_MIN + chaos
        if minimum < self.HARD_MIN:
            minimum = self.HARD_MIN
        if p < minimum:
            p=minimum
        return p
    class Meta:
        abstract = True

class Speaker(RememberDates):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name
    def speak(self,linePiece):
        return linePiece.speak(self)
    def chooseLine(self,lines):
        if lines.count() == 1:
            return lines[0]
        probabilities={}
        psum=0
        for line in lines:
            p=line.evaluate(self)
            probabilities[line]=p
            psum+=p
        i = randint(1,psum)
        for line in probabilities:
            i-=probabilities[line]
            if i < 1:
                return line

class SuperTrait(RememberDates):
    name=models.CharField(max_length=200, unique=True)
    opposite=models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.name

class Trait(RememberDates):
    type=models.ForeignKey(
        SuperTrait,
        on_delete=models.CASCADE,
        related_name='instances'
    )
    value=models.IntegerField(default=0)
    speaker=models.ForeignKey(
        Speaker,
        blank=True,
        on_delete=models.CASCADE,
        related_name='traits'
    )
    def __str__(self):
        return "%s (%s)"%(self.type, self.value)

class EvaluationFunction(RememberDates):
    trait=models.ForeignKey(
        SuperTrait,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='functions'
    )
    FUNCTION_TYPES = [
        ('TR','TRAIT'),
        ('RAW','RAW')
    ]
    type=models.CharField(max_length=10,choices=FUNCTION_TYPES)
    value=models.IntegerField()
    def __str__(self):
        return "%s / %s / %s"%(self.type, self.trait, self.value)
    def evaluate(self, traits):
        p=0
        try:
            if self.type=='TR':
                trait=traits.get(type=self.trait)
                value=trait.value
                p+=value*self.value
            elif self.type=='RAW':
                p+=self.value
        except Exception as e:
            pass

        return p

class LinePiece(Evaluetable):
    name=models.CharField(
        max_length=200,
        blank=True
    )
    text=NonStrippingTextField(blank=True)
    parent=models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='children'
    )
    altParent=models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='altChildren'
    )
    functions=models.ManyToManyField(
        EvaluationFunction,
        blank=True,
        related_name='linePieces'
    )
    order=models.IntegerField(default=0)
    def __str__(self):
        if self.name:
            if self.text:
                return "%s ('%s')"%(self.name, self.text)
            else:
                return self.name
        else:
            return "'%s'"%self.text

    def speak(self, speaker=None):
        # - 1 - altChildren ? - #
        if self.altChildren.all():
            altChildren=self.altChildren.all()
            if altChildren.count() == 1:
                return altChildren[0].speak(speaker)
            probabilities={}
            psum=0
            for a in altChildren:
                if not speaker:
                    p=1
                else:
                    p=a.evaluate(speaker)
                probabilities[a]=p
                psum+=p

            i = randint(1,psum)

            for a in probabilities:
                i-=probabilities[a]
                if i < 1:
                    return a.speak(speaker)
        # - 2 - children ? - #
        if self.children.all():
            children=self.children.all().order_by('order')
            finalString=''
            for c in children:
                finalString+=c.speak(speaker)
            return finalString
        # - 3 - text ? - #
        if self.text:
            return self.text
        # - 4 - nope - #
        return ''


class Conversation(RememberDates):
    name=models.CharField(max_length=200, blank=True)
    description=models.TextField(blank=True)
    def __str__(self):
        return self.name

class Line(Evaluetable):
    description=models.TextField(blank=True)
    pieces=models.ManyToManyField(LinePiece)
    answerTo=models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='answers'
    )
    answerTo_extra=models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='answers_extra'
    )

    functions=models.ManyToManyField(
        EvaluationFunction,
        blank=True,
        related_name='lines'
    )
    startsConversation= models.ForeignKey(
        Conversation,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='startline'
    )
    def speak(self, speaker=None):
        returnstring = ''
        for piece in self.pieces.all():
            returnstring += piece.speak(speaker)
        mparts=re.split('(\?|\!|\.)', returnstring)
        returnstring_=''
        for m in mparts:
            returnstring_+=m.capitalize()
        return returnstring_
    def __str__(self):
        return self.description
