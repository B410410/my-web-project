from django.http import HttpResponse, Http404
from shop.models import Product
import logging

# 設置錯誤日誌
logger = logging.getLogger(__name__)

def detail(request, id):
    try:
        p = Product.objects.get(id=id)
        rows = '<tr><td>商品編號</td><td>商品名稱</td><td>介紹</td><td>價錢</td><td>圖片</td></tr>'
        rows += f'<tr><td>{p.id}</td>'
        rows += f'<td>{p.name}</td>'
        rows += f'<td>{p.description}</td>'
        rows += f'<td>{int(p.price)}</td>'
        # 假設圖片存儲的是相對 URL，使用 <img> 標籤顯示圖片
        rows += f'<td><img src="{p.image.url}" alt="{p.name}" width="100"></td></tr>'

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{p.name}</title>
        </head>
        <body>
            <h2>{p.name}</h2>
            <hr>
            <table width="400" border="1" bgcolor="#ccffcc">
                {rows}
            </table>
        </body>
        </html>
        """

        return HttpResponse(html, status=200)

    except Product.DoesNotExist as e:
        # 當找不到該產品時，返回 404 Not Found
        logger.error(f"未找到產品: {e}")
        raise Http404(f"未找到產品編號{id}的商品")
        # return HttpResponse(f"產品編號{p.id}未找到", status=404)
    except ValueError as e:
        # 當請求的參數無效（例如產品 ID 不是有效的數字）時，返回 400 Bad Request
        logger.error(f"商品資訊無效: {e}")
        return HttpResponse(f"產品編號{id}無效", status=400)
    
    except Exception as e:
        # 當有其他未捕獲的錯誤時，返回 500 Internal Server Error
        logger.error(f"商品列表錯誤: {e}")
        return HttpResponse("發生錯誤，請稍後再試！", status=500)