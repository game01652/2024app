# Copyright 2022 Kokai Sakaguchi
# ビュー

from django.shortcuts import render, redirect
import requests
import random
from .forms import BookForm, StageForm, LanguageForm, CategoryForm, UserForm, AccountForm
from .models import Book, Stage, Language, Category
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# 書籍情報が格納されたリストから必要な情報だけを抜き取る。
def get_book(items_list):
    data = []    # 得られた書籍情報の中の必要な情報だけを格納する。

    # 必要な情報だけを取り出してdataに格納。
    for items in items_list:
        info = items["volumeInfo"]
        dic = {}    # 書籍情報の各項目を格納する辞書型データ。

        if 'id' not in items.keys():    # ID
            id = ""
        else:
            id = items['id']

        if 'title' not in info.keys():    # タイトル。
            title = ""
        else:
            title = info['title']
            title = title.replace('/', '・')    # タイトル名に「/」があれば、「・」に置き換える。（URLパラメータの関係より）

        if 'authors' not in info.keys():    # 著者。
            author = ""
        else:
            author = info['authors'][0]

        if 'publishedDate' not in info.keys():    # 出版日。
            publishedDate = ""
        else:
            publishedDate = info['publishedDate']

        if 'imageLinks' not in info.keys():    # 表紙画像のアドレス。
            bookCover = ""
        else:
            bookCover = info['imageLinks']['smallThumbnail']

        if 'description' not in info.keys():    # あらすじ。
            description = ""
        else:
            description = info['description']

        if 'pageCount' not in info.keys():    # ページ数。
            page = ""
        else:
            page = info['pageCount']

        if 'categories' not in info.keys():    # カテゴリー。
            category = ""
        else:
            category = info['categories'][0]

        if 'language' not in info.keys():    # 言語。
            language = ""
        else:
            language = info['language']

        if 'industryIdentifiers' not in info.keys():    # ISBN。
            isbn = ""
        else:
            a = info['industryIdentifiers']
            isb = a[0]
            isbn = isb['identifier']

        # 各項目を辞書に格納し、リストに追加する。
        dic["id"] = id
        dic["title"] = title
        dic["author"] = author
        dic["publishedDate"] = publishedDate
        dic["bookCover"] = bookCover
        dic["description"] = description
        dic["page"] = page
        dic["category"] = category
        dic["language"] = language
        dic["isbn"] = isbn
        data.append(dic)

    return data    # 書籍情報の返却。


# APIでの書籍検索ページのビュー。
def bookSearchView(request):
    template_name = "bookSearch.html"    # テンプレートファイル。
    form = BookForm(request.POST or None)    # 書籍を登録するためのフォームの初期化。

    # テンプレートで表示するデータ。
    app_data = {
        'form': form, 
    }

    return render(request, template_name, app_data)


# APIでの書籍一覧ページのビュー。
def bookListView(request):
    template_name = "bookList2.html"    # テンプレートファイル。
    data = []    # 書籍情報を格納するリスト。
    form = BookForm(request.POST or None)    # 書籍を登録するためのフォームの初期化。

    if request.method == 'POST':
        # formで得られた値を取得。
        title = form.data['title']
        author = form.data['author']
        isbn = form.data['isbn']

        url = "https://www.googleapis.com/books/v1/volumes?q="    # GooglBooksAPIの元となるURL。

        # Web-APIにアクセスするためのURLを作成。
        if title:
            url += "intitle:"
            url += title
        if author:
            url += "+inauthor:"
            url += author
        if isbn:
            url += "+isbn:"
            url += isbn
        url += "&maxResults=40"    # 取得する書籍を40件までに限定。

        try:    # 通常処理。
            response = requests.get(url).json()    # 書籍情報の取得し、json形式に変換。

            if 'totalItems' not in response.keys():
                book_len = 0
            else:
                book_len = response["totalItems"]
                if 'items' in response.keys():
                    data = get_book(response["items"])    # 得られた書籍情報の中の必要な情報だけを格納する。

        except requests.exceptions.RequestException as e:    # 例外処理。
            return redirect('BookApp:myBook')    # マイページのビューにリダイレクトする。

    # テンプレートで表示するデータ。
    myapp_data = {
        'total': book_len,
        'obj': data,
        'title': title,
        'author': author,
        'isbn': isbn,
        'form': form,
    }

    return render(request, template_name, myapp_data)


# APIでの書籍詳細ページのビュー。
@login_required    # ログイン状態であるかを判定する。
def bookDetailView(request, pk):
    template_name = "bookDetail.html"    # テンプレートファイル。

    try:
        # データベースに保存
        if pk == 2:
            form = BookForm(request.POST, request.FILES)    # フォームの内容を取得。
            form.save()    # フォームで取得した値をデータベースに保存。
            return redirect('BookApp:myBook')    # マイページにリダイレクトする。
        elif pk == 1:
            # フォームの初期化情報
            print(request.POST.get('param-title'))
            initial_dict = {
                'title': request.POST.get('param-title'),
                'author': request.POST.get('param-author'),
                'publishedDate': request.POST.get('param-publishedDate'),
                'description': request.POST.get('param-description'),
                'isbn': request.POST.get('param-isbn'),
                'page': request.POST.get('param-page'),
                'order' : len(Book.objects.filter(user=request.user.id)) + 1,
                'category': request.POST.get('param-category'),
                'language': request.POST.get('param-language'),
            }

            form = BookForm(initial=initial_dict)    # 登録するための書籍情報のフォームを初期化
    except:
        return redirect('BookApp:myBook')    # マイページにリダイレクトする。

    # テンプレートで表示するデータ。
    myapp_data = {
        'bookCover_url': request.POST.get('param-image'),
        'form': form,
    }

    return render(request, template_name, myapp_data)


# マイページのビュー。
@login_required    # ログイン状態であるかを判定する。
def myBookView(request):
    template_name = "myBook.html"    # テンプレートファイル。

    try:    # 通常処理。
        # データベースに保存
        if request.method == 'POST':
            form = BookForm(request.POST, request.FILES)    # フォームの内容を取得。
            if form.data['title']:
                obj = Book.objects.filter(title=form.data['title'])    # 特定のユーザの全書籍データの取得。
            elif form.data['author']:
                obj = Book.objects.filter(author=form.data['author'])    # 特定のユーザの全書籍データの取得。
            elif form.data['isbn']:
                obj = Book.objects.filter(isbn=form.data['isbn'])    # 特定のユーザの全書籍データの取得。
            elif form.data['review']:
                obj = Book.objects.filter(review=form.data['review'])    # 特定のユーザの全書籍データの取得。
            elif form.data['order']:
                obj = Book.objects.filter(order=form.data['order'])    # 特定のユーザの全書籍データの取得。
            elif form.data['category']:
                obj = Book.objects.filter(category=Category.objects.filter(id=form.data['category'])[0].id)    # 特定のユーザの全書籍データの取得。
            elif form.data['language']:
                obj = Book.objects.filter(language=Language.objects.filter(id=form.data['language'])[0].id)    # 特定のユーザの全書籍データの取得。
            elif form.data['stage']:
                obj = Book.objects.filter(stage=Stage.objects.filter(id=form.data['stage'])[0].id)    # 特定のユーザの全書籍データの取得。

        else:
            obj = Book.objects.filter(user=request.user.id).order_by('order').reverse()    # 現在、ログインしているユーザの全書籍データの取得。
            form = BookForm(request.POST or None)    # 書籍を登録するためのフォームの初期化。
    except:
        return redirect('BookApp:myBook')    # マイページにリダイレクトする。

    for item in obj:
        if item.registerDate is not None:
            item.registerDate = item.registerDate.strftime('%Y-%m-%d %H:%M:%S')
        if item.updateDate is not None:
            item.updateDate = item.updateDate.strftime('%Y-%m-%d %H:%M:%S')
 
    # テンプレートで表示するデータ。
    myapp_data = {
        'total': len(obj),
        'obj': obj,
        'form': form,
    }

    return render(request, template_name, myapp_data)


# データベース上の全書籍一覧のビュー。
def allBookView(request):
    template_name = "allBook.html"    # テンプレートファイル。

    obj = Book.objects.all().order_by('order').reverse()    # データベースに登録されている全書籍データの取得。

    # テンプレートで表示するデータ。
    myapp_data = {
        'total': len(obj),
        'obj': obj,
    }

    return render(request, template_name, myapp_data)


# マイブックの詳細ページのビュー。
@login_required    # ログイン状態であるかを判定する。
def myBookDetailView(request, id):
    template_name = "myBookDetail.html"    # テンプレートファイル。

    obj = Book.objects.get(pk=id)    # 取得したIDに該当する書籍データの取得。

    # フォームの初期化情報
    initial_dict = {
        'title': obj.title,
        'author': obj.author,
        'publishedDate': obj.publishedDate,
        'description': obj.description,
        'isbn': obj.isbn,
        'page': obj.page,
        'registerDate' : obj.registerDate,
        'impression' : obj.impression,
        'review' : obj.review,
        'order' : obj.order,
        'stage' : obj.stage,
        'category': obj.category,
        'language': obj.language,
    }

    form = BookForm(request.POST or None, initial=initial_dict)    # 書籍を登録するためのフォームの初期化。

    # テンプレートで表示するデータ。
    myapp_data = {
        'obj': obj,
        'form': form,
    }

    return render(request, template_name, myapp_data)


# 書籍の削除を行うビュー。
@login_required    # ログイン状態であるかを判定する。
def myBookDeleteView(request):
    try:    # 通常処理。
        result = request.POST.getlist('delete')
        Book.objects.filter(id__in=result).delete()    # 書籍の削除。
    except:    # 例外処理。
        return redirect('BookApp:myBook')    # マイページにリダイレクトする。

    return redirect('BookApp:myBook')    # マイページにリダイレクトする。


# 書籍の更新を行うビュー。
@login_required    # ログイン状態であるかを判定する。
def myBookUpdateView(request, id):
    try:    # 通常処理。
        member = get_object_or_404(Book, id=id)    # 取得したIDに該当する書籍データの取得。
        if request.method == "POST":
            form = BookForm(request.POST, request.FILES, instance=member)    # フォームの取得。
            if form.is_valid():
                form.save()    # 書籍データの更新。
    except:    # 例外処理。
        return redirect('BookApp:myBook')    # マイページにリダイレクトする。

    return redirect('BookApp:myBook')    # マイページにリダイレクトする。


# 書籍を一から登録する画面のビュー。
@login_required    # ログイン状態であるかを判定する。
def newBookView(request):
    template_name = "newBook.html"    # テンプレートファイル。

    try:    # 通常処理。
        if request.method == 'POST':
            form = BookForm(request.POST, request.FILES)    # フォームの取得。
            if form.is_valid():
                form.save()    # 書籍を登録する。
            return redirect('BookApp:myBook')    # マイページにリダイレクトする。
        else:
            # フォームの初期化情報
            initial_dict = {
            'order' : len(Book.objects.filter(user=request.user.id)) + 1,
            }
            form = BookForm(initial=initial_dict)    # 登録するための書籍情報のフォームを初期化

    except:    # 例外処理。
        return redirect('BookApp:myBook')    # マイページにリダイレクトする。

    # テンプレートで表示するデータ。
    myapp_data = {
        'form': form,
    }

    return render(request, template_name, myapp_data)


# ログインを行うビュー。
def loginView(request):
    template_name = "login.html"    # テンプレートファイル。

    form = AccountForm(request.POST or None)    # 書籍を登録するためのフォームの初期化。

    # テンプレートで表示するデータ。
    myapp_data = {
        'form': form,
    }

    myapp_data_error = {
        'error': 'There are no user you logined.',
        'form': form,
    }

    if request.method == 'POST':
        user = authenticate(request, username=form.data['username'], password=form.data['password'])    # ユーザデータの照合。

        if user is not None:    # ログインしようとしたユーザがいる場合。
            login(request, user)    # ログイン処理。
            return redirect('BookApp:myBook')    # マイページにリダイレクトする。
        else:    # ユーザがいない場合。
            return render(request, template_name, myapp_data_error)

    return render(request, template_name, myapp_data)


# ログアウトを行うビュー。
def logoutView(request):
    logout(request)    # ログアウト。
    return redirect('BookApp:login')    # ログイン画面にリダイレクトする。





# 書籍の読書進捗段階を新規作成するビュー。
@login_required    # ログイン状態であるかを判定する。
def contentCreateView(request, id):
    template_name = "contentCreate.html"    # テンプレートファイル。

    if request.method == 'POST':
        if id == 'stage-create':
            form = StageForm(request.POST or None)    # フォームの内容を取得。
        elif id == 'language-create':
            form = LanguageForm(request.POST or None)    # フォームの内容を取得。
        elif id == 'category-create':
            form = CategoryForm(request.POST or None)    # フォームの内容を取得。

        form.save()    # フォームで取得した値をデータベースに保存。
        return redirect('BookApp:allContent')    # ログイン画面にリダイレクトする。
    else:
        if id == 'stage-create':
            form = StageForm(request.POST or None)
            obj = Stage.objects.order_by('id').reverse()    # 全進捗段階のリスト。
            flag = 'stage-create'
        elif id == 'language-create':
            form = LanguageForm(request.POST or None)
            obj = Language.objects.order_by('id').reverse()    # 全進捗段階のリスト。
            flag = 'language-create'
        elif id == 'category-create':
            form = CategoryForm(request.POST or None)
            obj = Category.objects.order_by('id').reverse()    # 全進捗段階のリスト。
            flag = 'category-create'

        # テンプレートで表示するデータ。
        myapp_data = {
            'form': form,
            'obj': obj,
            'flag': flag,
        }

        return render(request, template_name, myapp_data)


# ステージの削除を行うビュー。
@login_required    # ログイン状態であるかを判定する。
def contentDeleteView(request, id, flag):
    try:    # 通常処理。
        if flag == 'stage':
            result = Stage.objects.filter(id=id)    # 取得したIDに該当する書籍データの取得。
        elif flag == 'language':
            result = Language.objects.filter(id=id)    # 取得したIDに該当する書籍データの取得。
        elif flag == 'category':
            result = Category.objects.filter(id=id)    # 取得したIDに該当する書籍データの取得。

        result.delete()    # 書籍の削除。
    except:    # 例外処理。
         return redirect('BookApp:allContent')    # マイページにリダイレクトする。

    return redirect('BookApp:allContent')    # マイページにリダイレクトする。


# 書籍の更新を行うビュー。
@login_required    # ログイン状態であるかを判定する。
def contentUpdateView(request, id, flag):
    try:    # 通常処理。
        if request.method == "POST":
            if flag == 'stage':
                member = get_object_or_404(Stage, id=id)    # 取得したIDに該当する書籍データの取得。
                form = StageForm(request.POST, request.FILES, instance=member)    # フォームの取得。
            elif flag == 'language':
                member = get_object_or_404(Language, id=id)    # 取得したIDに該当する書籍データの取得。
                form = LanguageForm(request.POST, request.FILES, instance=member)    # フォームの取得。
            elif flag == 'category':
                member = get_object_or_404(Category, id=id)    # 取得したIDに該当する書籍データの取得。
                form = CategoryForm(request.POST, request.FILES, instance=member)    # フォームの取得。

            if form.is_valid():
                form.save()    # 書籍データの更新。
    except:    # 例外処理。
        return redirect('BookApp:allContent')    # マイページにリダイレクトする。

    return redirect('BookApp:allContent')    # マイページにリダイレクトする。



# 書籍の更新を行うビュー。
@login_required    # ログイン状態であるかを判定する。
def allContentView(request):
    template_name = "allContent.html"    # テンプレートファイル。

    stage = Stage.objects.order_by('id').reverse()    # 全進捗段階のリスト。
    language = Language.objects.order_by('id').reverse()    # 全進捗段階のリスト。
    category = Category.objects.order_by('id').reverse()    # 全進捗段階のリスト。

    # テンプレートで表示するデータ。
    myapp_data = {
        'stage': stage,
        'language': language,
        'category': category,
    }

    return render(request, template_name, myapp_data)


# 書籍の読書進捗段階を新規作成するビュー。
@login_required    # ログイン状態であるかを判定する。
def userInformationView(request):
    template_name = "userInformation.html"    # テンプレートファイル。

    obj = User.objects.get(id=request.user.id)    # 取得したIDに該当する書籍データの取得。

    # テンプレートで表示するデータ。
    myapp_data = {
        'obj': obj,
    }

    return render(request, template_name, myapp_data)


# 書籍の更新を行うビュー。
@login_required    # ログイン状態であるかを判定する。
def userUpdateView(request):
    template_name = "userUpdate.html"    # テンプレートファイル。

    member = get_object_or_404(User, id=request.user.id)    # 取得したIDに該当する書籍データの取得。

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=member)    # フォームの取得。
        if form.is_valid():
            form.save()    # 書籍データの更新。
        return redirect('BookApp:userInformation')    # マイページにリダイレクトする。
    else:
        obj = User.objects.get(id=request.user.id)    # 取得したIDに該当する書籍データの取得。

        # フォームの初期化情報
        initial_dict = {
            'username': obj.username,
            'email': obj.email,
            'first_name': obj.first_name,
            'last_name': obj.last_name,
        }

        form = UserForm(request.POST or None, initial=initial_dict)    # 書籍を登録するためのフォームの初期化。

        # テンプレートで表示するデータ。
        myapp_data = {
            'form': form,
            'obj': obj,
        }

        return render(request, template_name, myapp_data)
