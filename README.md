### The Dockerized version of the EOMF website
#### [Link to the site](http://eomf.ou.edu/)  

---



**Regarding the style of imports in url.py files**

At the time of writing, I am completely rewriting the 10 year old url.py files, and after much deliberation I've decided the style I'm going to use is:
```
import eomf.birds.views

urlpatterns = [
    re_path(r'^$', eomf.birds.views.index),
]
```
Most enterprise developers would likely write this as:
```
import eomf.birds.views as views

urlpatterns = [
    re_path(r'^$', views.index),
]
```
or
```
from eomf import birds.views

urlpatterns = [
    re_path(r'^$', birds.views.index),
]
```
However, in the first one the `eomf.birds.views` syntax is shared by each usage, which means it can be copy-pasted. This is very helpful, as I have to fix every url.py file, and  hundreds of url patterns.
