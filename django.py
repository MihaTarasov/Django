#Тут все,что вы просили скинуть связаное с моей проблемой

#Форма
class PostForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
    class Meta:
        model = News
        fields = ['title','text','category']

        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Заголовок'}),
            'text':forms.Textarea(attrs={'class':'form-control','placeholder':'Текст'}),
        } 
       
#это url создания поста
path('create/',Create.as_view(),name='create'),


#это его класс-обработчик url-a выше  (LoginRequiredMixin-миксни для ограничения досутпа т.е если пользователь не админ,то не сможет видеть определенную страницу )
#CreateMixin - миксни это класса (ниже)
class Create(LoginRequiredMixin,CreateMixin,View):
    template_name = 'blog/create_post.html'
    model = News
    redirect_page = 'list'
    form = PostForm

#Миксин класса Create

class CreateMixin(View):
    model = None #модель 
    form = None #форма
    redirect_page = None #перенаправление пользователся после создание поста
    template_name = None #шаблон
    
    def get(self,request):
        forms = self.form()
        return render(request,self.template_name,context={'forms':forms})
    def post(self,request):
        form_post = self.form(request.POST)
        if form_post.is_valid():
            form_post.save()
            return redirect(self.redirect_page)
        return render(request,self.template_name,context={'forms':form_post})

#модель постов

class News(models.Model):
    title = models.CharField('Заголовок',max_length=70)
    text = models.TextField('Текст',blank=True)
    created_ut = models.DateTimeField('Дата публикации',auto_now_add=True,)
    updated_ut = models.DateTimeField('Дата изменения',auto_now=True)
    photo = models.ImageField('Фото',upload_to='photos/%Y/%m/%d',blank=True)
    is_published = models.BooleanField('Публикация на сайт',default=True)
    category = models.ForeignKey('Category',on_delete=models.PROTECT,null=True,verbose_name='Категория',related_name='news')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
                    

