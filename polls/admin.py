from django.contrib import admin
from .models import User
from .models import Pool
from .models import Group
from .models import Choice
import xlwt
from django.http import StreamingHttpResponse
from datetime import datetime
from .models import Dictionary
# Register your models here.
admin.site.site_header = '后台管理系统'
admin.site.site_title = '后台管理中心'


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'last_login_ip', 'last_login_time', 'status')
    list_filter = ['username', 'email']
    search_fields = ['username', 'email']
    list_per_page = 10


class PoolAdmin(admin.ModelAdmin):
    # readonly_fields=('image_tag',)
    list_display = ('id', 'title', 'group_name', 'image_tag')
    list_display_links = ('image_tag',)
    list_filter = ['group_id', ]
    list_per_page = 10


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_name')
    list_per_page = 10


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('username', 'use_time', 'leftTitle', 'left_pic', 'rightTitle', 'right_pic', 'choice_num', 'choose_time')
    list_per_page = 10
    list_display_links = ('left_pic', 'right_pic')
    list_filter = (
        'user_id',
        'choose_time',
    )
    actions = ["SaveExcel", ]

    def SaveExcel(self, request, queryset):
        TYPE_CHOICES = ['', '左图更优', '右图更优', '两图相似']
        Begin = xlwt.Workbook()
        sheet = Begin.add_sheet("response")
        sheet.write(0, 0, '标注人员')
        sheet.write(0, 1, '操作时间')
        sheet.write(0, 2, '左边图片名称')
        sheet.write(0, 3, '右边图片名称')
        sheet.write(0, 4, '选择记录')
        sheet.write(0, 5, '时间')
        cols = 1
        for query in queryset:
            # you need write colms                     # 好像有个方法可以一次性写入所有列，记不清了，只能用这种简单的方法去实现
            sheet.write(cols, 0, str(query.username))  # 写入第一列
            sheet.write(cols, 1, str(query.use_time))  # 写入第二列
            sheet.write(cols, 2, str(query.leftTitle))  # 写入第三列
            sheet.write(cols, 3, str(query.rightTitle))
            sheet.write(cols, 4, TYPE_CHOICES[query.choice_num])
            #sheet.write(cols, 5, str(query.choose_time)[0:19])
            sheet.write(cols, 5, datetime.strftime(query.choose_time,"%Y-%m-%d %H:%M:%S"))
            cols += 1
        Begin.save("D:\Records-"+datetime.now().strftime("%Y%m%d%H%M%S")+".xls")

        def file_iterator(filename, chunk_size=512):
            with open(filename, 'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        response = StreamingHttpResponse(file_iterator("D:\Records-"+datetime.now().strftime("%Y%m%d%H%M%S")+".xls"))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename="{}" '.format("Records-"+datetime.now().strftime("%Y%m%d%H%M%S")+".xls")
        return response

    SaveExcel.short_description = "以表格形式下载"


class DictionaryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'data_name', 'data_value',
    )


admin.site.register(Dictionary, DictionaryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Pool, PoolAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Choice, ChoiceAdmin)



