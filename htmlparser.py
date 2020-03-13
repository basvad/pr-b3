#реализация класса HTML
class HTML:
    def __init__(self, output=None):
        self.output = output
        self.tag = "html"
        self.children=[]
    def __enter__(self):
        return(self)
    def __exit__(self, type, value, traceback):
        if self.output is not None:
            s=str(self.output)+"/test.html"
            with open(s, "w") as f:
                f.write(str(self))
        else:
            childtag="\n".join(self.children)
            print("<{tag}>\n{childtag}\n</{tag}>".format(tag=self.tag , childtag=childtag))
    def __str__(self):
        childtag="\n".join(self.children)
        return "<{tag}>\n{childtag}\n</{tag}>".format(tag=self.tag , childtag=childtag)
    def __add__(self, other):
        childtag=" \n".join(other.children)
        self.children.append("\t<{tag}>\n{childtag}\n\t</{tag}>".format(tag=other.tag, childtag=childtag))
        return self

#реализация класса TopLevelTag
class TopLevelTag:
    def __init__(self, tag):
        self.tag = tag
        self.attributes = {}
        self.children  = []
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        attrs = []
        for attribute, value in self.attributes.items():
            #добавили атрибуты в список
            attrs.append('%s="%s"' % (attribute, value))
        #формирует строку через пробел
        attrs = " ".join(attrs)
        childtag=" \n".join(self.children)
        return "<{tag} {attrs}>\n{childtag}\n</{tag}>".format(tag=self.tag, attrs=attrs, childtag=childtag)
        
    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            #добавили атрибуты в список
            attrs.append('%s="%s"' % (attribute, value))
        #формирует строку через пробел
        attrs = " ".join(attrs)
        childtag=" \n".join(self.children)
        return "<{tag} {attrs}>\n{childtag}\n</{tag}>".format(tag=self.tag, attrs=attrs, childtag=childtag)
    
    def __add__(self, other):
        other_attrs = []
        for attribute, value in other.attributes.items():
            other_attrs.append('%s="%s"' % (attribute, value))
        other_attrs = " ".join(other_attrs)
        if self.children:
            childtag=" \n".join(other.children)
            other_tag="\t<{tag} {attrs}> {text}\n{childtag}\n\t</{tag}>".format(tag=other.tag, attrs=other_attrs, text=other.text, childtag=childtag)
        else:
            other_tag="\t<{tag} {attrs}> {text} </{tag}>".format(tag=other.tag, attrs=other_attrs, text=other.text)
        self.children.append(other_tag)
        return self      
		
#реализация класса Tag
class Tag:
    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.children  = []
        self.is_single = is_single
        
         #заполняем класс
        if klass is not None:
            self.attributes["class"] = " ".join(klass)
        #заполняем переданные аттрибуты
        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
        if self.children:
            if self.is_single:
                return "<\t{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)
            else:
                childtag=" \n".join(self.children)
                return  "<\t{tag} {attrs}> {text}\n{childtag}\n\t</{tag}>".format(tag=self.tag, attrs=attrs, text=self.text,childtag=childtag)

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            #добавили атрибуты в список
            attrs.append('%s="%s"' % (attribute, value))
        #формирует строку через пробел
        attrs = " ".join(attrs)
        if self.is_single:
            return "<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)
        else:
            return "<{tag} {attrs}>{text}</{tag}>".format(tag=self.tag, attrs=attrs, text=self.text)
    
    def __add__(self, other):
        other_attrs = []
        for attribute, value in other.attributes.items():
            other_attrs.append('%s="%s"' % (attribute, value))
        other_attrs = " ".join(other_attrs)
        if other.is_single:
            other_tag = "\t\t<{tag} {attrs}/>".format(tag=other.tag, attrs=other_attrs)
        else:
            other_tag="\t\t<{tag} {attrs}> {text} </{tag}>".format(tag=other.tag, attrs=other_attrs, text=other.text)
        self.children.append(other_tag)
        return self  