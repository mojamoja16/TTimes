from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(ParentCompanyModel)
admin.site.register(StaffModel)
admin.site.register(AttendanceModel)

@admin.register(ChildCompanyModel)
class UserAdmin(UserAdmin):
    # http://127.0.0.1:8000/admin/TTimes/childcompanymodel/に何を表示するのか選ぶ場所です. emailやparent_companyを置いてもいいかも
    list_display =['name']
    # http://127.0.0.1:8001/admin/TTimes/childcompanymodel/<int:pk>/change/に何を表示するのか選ぶ場所です.
    # 4つに分かれます.
    ## None: 以降に続くPersonal info, Permissions, Important dates以外で表示したいものを選択します.
    ## Personal info: そのユーザーに関する情報を選ぶ場所です.本当はemailはここで良い気もします. 
    ## Permissions: 権限系を選択する場所です
    ## Important dates: 時間系です.
    ### 正直見出しで区切るだけなのでどのフィールドがどこにあっても構いません.見やすいか見やすくないかの違いだけです.
    fieldsets = (
        (None, {'fields': ('name','email', 'password')}),
        ('Personal info', {'fields': ('parent_company', )}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # http://127.0.0.0:8000/admin/TTimes/childcompanymodel/addに何を表示するか選ぶ場所です.
    # ユーザー作成時に必要になるname, passwordは必ず表示するようにします.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2'),
        }),
    )
    # ソートの対象フィールドを選択します.デフォルトでusernameが入っているようだったのでnameに上書きしました.
    ordering = ('name',)
    # http://127.0.0.0:8000/admin/TTimes/childcompanymodel/ の右側に「フィルター」というのがありますがそこに何を表示するか選択する場所です.
    # デフォルトでusernameが入っているようだったのでnameに上書きしました.
    list_filter = ('name', 'is_superuser', 'is_active', 'groups', )
    # http://127.0.0.0:8000/admin/TTimes/childcompanymodel/の検索ボックスで検索対象のフィールドを選択する場所です
    # デフォルトでusernameが入っているようだったのでnameに上書きしました.
    search_fields = ('name', )