import uuid


# Card types, according to https://developer.atlassian.com/hipchat/guide/sending-messages

class Card:
    def __init__(self, style: str, url: str = '', id: str = str(uuid.uuid4()), title='', format: str = 'medium'):
        available_styles = ['file', 'image', 'application', 'link', 'media']
        if style not in available_styles:
            raise ValueError("Style '" + style + "' is invalid. Available styles: " + str(available_styles))
        self.style = style

        available_formats = ['compact', 'medium']
        if format not in available_formats:
            raise ValueError("Format '" + format + "' is invalid. Available formats: " + str(available_formats))
        self.format = format

        self.url = url
        self.id = id
        self.title = title


class Icon:
    def __init__(self, url: str = ''):
        self.url = url


class AttributeValue:
    def __init__(self, label: str = '', icon: Icon = None, style: str = 'lozenge'):
        self.label = label
        if icon is not None:
            self.icon = icon.__dict__
        available_styles = ['lozenge-success', 'lozenge-error', 'lozenge-current',
                            'lozenge-complete', 'lozenge-moved', 'lozenge']
        if style not in available_styles:
            raise ValueError("Style '" + style + "' is invalid. Available styles: " + str(available_styles))
        self.style = style


class Attribute:
    def __init__(self, label='', value: AttributeValue = None):
        self.label = label
        if value is not None:
            self.value = value.__dict__


class Activity:
    def __init__(self, html: str = ''):
        self.html = html


class ApplicationCard(Card):
    def __init__(self, url: str = '', id: str = str(uuid.uuid4()), title='',
                 description: str = '', icon: Icon = None, attributes: list = None):
        super().__init__(style='application', format='medium', url=url, id=id, title=title)
        self.description = description
        if icon is not None:
            self.icon = icon.__dict__
        new_attributes = list()
        if attributes is not None:
            for attribute in attributes:
                new_attributes.append(attribute.__dict__)
            self.attributes = new_attributes


class ActivityCard(Card):
    def __init__(self, url: str = '', id: str = str(uuid.uuid4()), title='',
                 description: str = '', icon: Icon = None, attributes: list = None, activity: Activity = None):
        super().__init__(style='application', format='medium', url=url, id=id, title=title)
        self.description = description
        if icon is not None:
            self.icon = icon.__dict__
        new_attributes = list()
        if attributes is not None:
            for attribute in attributes:
                new_attributes.append(attribute.__dict__)
            self.attributes = new_attributes
        if activity is not None:
            self.activity = activity
