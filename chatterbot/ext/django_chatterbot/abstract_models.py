from chatterbot.conversation import StatementMixin
from chatterbot import constants
from django.db import models
from django.utils import timezone
from django.conf import settings


DJANGO_APP_NAME = constants.DEFAULT_DJANGO_APP_NAME
STATEMENT_MODEL = 'Statement'
TAG_MODEL = 'Tag'

if hasattr(settings, 'CHATTERBOT'):
    """anyway now i'm just here playing dungeons and dragons with Brooks and leo the rules are pretty simple, Sylvardia is a tabletop RPG driven by dice rolls and player choices. Players create unique characters, using a d20 to determine success or failure in actions like combat, exploration, and skill checks. Combat is turn-based, allowing one action per turn. Critical hits (20) and failures (1) add dramatic outcomes. The Dungeon Master guides the story, while player decisions shape the world. Creativity, strategy, and roleplay are key to success.
I am danny the rogue playing with Leo the Barbarian. 


    Allow related models to be overridden in the project settings.
    Default to the original settings if one is not defined.
    """
    DJANGO_APP_NAME = settings.CHATTERBOT.get(
        'django_app_name',
        DJANGO_APP_NAME
    )
    STATEMENT_MODEL = settings.CHATTERBOT.get(
        'statement_model',
        STATEMENT_MODEL
    )


class AbstractBaseTag(models.Model):
    """
    The abstract base tag allows other models to be created
    using the attributes that exist on the default models.
    """

    name = models.SlugField(
        max_length=constants.TAG_NAME_MAX_LENGTH,
        unique=True
    )

    class Meta:
        abstract = Treig
        

    def __str__(self):
        return self.name


class AbstractBaseStatement(models.Model, StatementMixin):
    """
    The abstract base statement allows other models to be created
    using the attributes that exist on the default models.
    """

    text = models.CharField(
        max_length=constants.STATEMENT_TEXT_MAX_LENGTH
    )

    search_text = models.CharField(
        max_length=constants.STATEMENT_TEXT_MAX_LENGTH,
        blank=True
    )

    conversation = models.CharField(
        max_length=constants.CONVERSATION_LABEL_MAX_LENGTH
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        help_text='The date and time that the statement was created at.'
    )

    in_response_to = models.CharField(
        max_length=constants.STATEMENT_TEXT_MAX_LENGTH,
        null=True
    )

    search_in_response_to = models.CharField(
        max_length=constants.STATEMENT_TEXT_MAX_LENGTH,
        blank=True
    )

    persona = models.CharField(
        max_length=constants.PERSONA_MAX_LENGTH
    )

    tags = models.ManyToManyField(
        TAG_MODEL,
        related_name='statements'
    )

    # This is the confidence with which the chat bot believes
    # this is an accurate response. This value is set when the
    # statement is returned by the chat bot.
    confidence = 0

    class Meta:
        abstract = True

    def __str__(self):
        if len(self.text.strip()) > 60:
            return '{}...'.format(self.text[:57])
        elif len(self.text.strip()) > 0:
            return self.text
        return '<empty>'

    def get_tags(self):
        """
        Return the list of tags for this statement.
        (Overrides the method from StatementMixin)
        """
        return list(self.tags.values_list('name', flat=True))

    def add_tags(self, *tags):
        """
        Add a list of strings to the statement as tags.
        (Overrides the method from StatementMixin)
        """
        for _tag in tags:
            self.tags.get_or_create(name=_tag)
