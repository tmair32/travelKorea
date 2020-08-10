from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Avg
from django.conf.urls import url
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import urllib.request, json, pprint
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Common, Detail, Bookmark, Score, Comment, Stamp
from .forms import ScoreForm, CommentForm
from .serializers import CommonSerializer, DetailSerializer, SearchByAreaSerializer, SearchBySigunguSerializer, \
    SearchByCategorySerializer, SearchByContentIdSerializer, ScoreSerailizer
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

# main page
def main(request):
    ServiceKey = "5Z64FYjCYoIRrToMriTzGi%2BbzlzcHOFJKdG9NFgR77i52r%2BCCi6XbU9gpq15l8fEGojdilIdq0iyzQvIpe3BlQ%3D%3D"
    url = "http://api.visitkorea.or.kr/openapi/service/rest/KorService/"
    key = "?ServiceKey=" + ServiceKey
    get = "areaCode"
    option = "&numOfRows=17&pageNo=1&MobileOS=AND&MobileApp=travel5&_type=json"
    url_ = url + get + key + option

    request_ = urllib.request.Request(url_)
    response = urllib.request.urlopen(request_)
    rescode = response.getcode()
    area = {
        '서울': '서울특별시',
        '인천': '인천광역시',
        '대전': '대전광역시',
        '대구': '대구광역시',
        '광주': '광주광역시',
        '부산': '부산광역시',
        '울산': '울산광역시',
        '제주도': '제주특별자치도'
    }
    if (rescode == 200):
        response_body = response.read()
        dict = json.loads(response_body.decode('utf-8'))
        value = dict['response']['body']['items']['item']
        # pprint.pprint(value)
        for item in value:
            if item['name'] in area.keys():
                value[item['rnum'] - 1]['name'] = area[item['name']]
        context = {'value': value}
        return render(request, 'maps/MainPage.html', context)
    else:
        print("Error Code:" + rescode)
        return render(request, 'maps/MainPage.html')


# 리뷰삭제
def deletereview(request, score_id):
    delscore = get_object_or_404(Score, contentId=score_id, user=request.user)
    print(delscore)
    delscore.delete()
    return redirect('maps:travelreview')


# 리뷰게시판 이동
def travelreview(request):
    ServiceKey = "5Z64FYjCYoIRrToMriTzGi%2BbzlzcHOFJKdG9NFgR77i52r%2BCCi6XbU9gpq15l8fEGojdilIdq0iyzQvIpe3BlQ%3D%3D"
    url = "http://api.visitkorea.or.kr/openapi/service/rest/KorService/"
    key = "?ServiceKey=" + ServiceKey
    get = "areaCode"
    option = "&numOfRows=17&pageNo=1&MobileOS=AND&MobileApp=travel5&_type=json"
    url_ = url + get + key + option

    request_ = urllib.request.Request(url_)
    response = urllib.request.urlopen(request_)
    rescode = response.getcode()
    area = {
        '서울': '서울특별시',
        '인천': '인천광역시',
        '대전': '대전광역시',
        '대구': '대구광역시',
        '광주': '광주광역시',
        '부산': '부산광역시',
        '울산': '울산광역시',
        '제주도': '제주특별자치도'
    }
    if (rescode == 200):
        response_body = response.read()
        dict = json.loads(response_body.decode('utf-8'))
        value = dict['response']['body']['items']['item']
        # pprint.pprint(value)
        for item in value:
            if item['name'] in area.keys():
                value[item['rnum'] - 1]['name'] = area[item['name']]
    else:
        print("Error Code:" + rescode)
        return render(request, 'maps/MainPage.html')

    page_data = Paginator(Score.objects.all(), 10)
    page = request.GET.get('page')
    if page is None:
        page = 1
    try:
        scores = page_data.page(page)
    except PageNotAnInteger:
        scores = page_data.page(1)
    except EmptyPage:
        scores = page_data.page(page_data.num_pages)

    context = {'scores': scores, 'cur_page': int(page), 'total_page': range(1, (page_data.num_pages + 1)),
               'value': value}
    return render(request, 'maps/travelReview.html', context)


# comment 달기
@require_http_methods(['POST'])
def create_comment(request, detail_id):
    common_inform = get_object_or_404(Common, contentId=detail_id)
    user = request.user
    if request.user.is_authenticated:
        if request.method == "POST":
            comment = CommentForm(request.POST)
            if comment.is_valid():
                print("D")
                comment = comment.save(commit=False)
                comment.user = user
                comment.inform = common_inform
                comment.contentId = detail_id
                comment.save()
                return redirect('maps:detailpage', detail_id)
        return redirect('maps:detailpage', detail_id)
    else:
        return redirect('maps:detailpage', detail_id)



def detailpage(request, detail_id=0):
    common = get_object_or_404(Common, contentId=detail_id)
    avg = common.score_set.all().aggregate(Avg('score'))
    comments = Comment.objects.filter(contentId=detail_id).order_by('-createdAt')
    comment_form = CommentForm()
    if (request.user.is_authenticated):
        scoreChk = Score.objects.filter(user_id=request.user.email, contentId=detail_id).exists()
        if scoreChk == False:
            score_form = ScoreForm()
        else:
            score, created = Score.objects.get_or_create(user_id=request.user.email, inform=common)
            score_form = ScoreForm(instance=get_object_or_404(Score, contentId=detail_id, user_id=request.user.email))
        if Bookmark.objects.filter(inform=common, user=request.user).exists():
            flag = "true"
        else:
            flag = "false"

        context = {"contentid": detail_id, 'flag': flag, "avg": avg, 'score_form': score_form, 'common': common,
                   "comment_form": comment_form, 'comments': comments}
        return render(request, 'maps/DetailPage.html', context)
    else:
        score_form = ScoreForm()
        flag = "false"
        context = {"contentid": detail_id, 'flag': flag, "avg": avg, 'score_form': score_form, 'common': common,
                   "comment_form": comment_form, 'comments': comments}
        return render(request, 'maps/DetailPage.html', context)


def scoreboard(request, detail_id=0):
    common = get_object_or_404(Common, contentId=detail_id)
    score = Score.objects.filter(user_id=request.user.email, contentId=detail_id).exists()
    if score == False:
        score_form = ScoreForm()
    else:
        score_form = ScoreForm(instance=get_object_or_404(Score, contentId=detail_id, user_id=request.user.email))
    context = {"contentid": detail_id, 'score_form': score_form, 'common': common}
    return render(request, 'maps/Detailpage.html', context)


@csrf_exempt
def addscore(request, detail_id=0):
    common = get_object_or_404(Common, contentId=detail_id)
    score, created = Score.objects.get_or_create(user_id=request.user.email, inform=common)
    stamp = Stamp.objects.get_or_create(user=request.user, inform=common)
    if request.method == "POST":
        score_form = ScoreForm(request.POST, instance=score)
        if score_form.is_valid():
            score = score_form.save(commit=False)
            score.contentId = detail_id
            score.inform = common
            score.user = request.user
            score.save()
            return redirect('maps:detailpage', detail_id)
    else:
        score_form = ScoreForm()
    context = {"contentid": detail_id, 'score_form': score_form}
    return render(request, 'maps/DetailPage.html', context)


@csrf_exempt
def bookmark(request, detail_id):
    common = get_object_or_404(Common, contentId=detail_id)
    flag = ""
    if Bookmark.objects.filter(inform=common, user=request.user).exists():
        bookmark = Bookmark.objects.get(inform=common, user=request.user)
        bookmark.delete()
        flag = "false"
    else:
        bookmark = Bookmark(
            user=request.user,
            inform=common,
            contentType=common.category
        )
        bookmark.save()
        flag = "true"

    redirect_to = reverse('maps:detailpage', kwargs={'detail_id': detail_id})
    return HttpResponseRedirect(redirect_to, {'flag': flag})


@api_view(['GET'])
def commonserializers(request):
    '''
    공통정보 출력
    '''
    commons = Common.objects.all()
    serializer = CommonSerializer(commons, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def searchbyareaserializers(request, area, category):
    '''
    지역코드로 정보 가져오기
    '''
    commons = Common.objects.filter(area=area, category=category)
    serializer = SearchByAreaSerializer(commons, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def searchbysigunguserializers(request, area, sigungu, category):
    '''
    지역코드, 시군구 코드로 정보 가져오기
    '''
    commons = Common.objects.filter(area=area, sigungu=sigungu, category=category)
    serializer = SearchBySigunguSerializer(commons, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def searchbycategoryserializers(request, category):
    '''
    카테고리로 정보 가져오기
    '''
    commons = Common.objects.filter(category=category)
    serializer = SearchByCategorySerializer(commons, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def searchbycontentidserializers(request, contentid):
    '''
    contentid로 정보 가져오기
    '''
    commons = Common.objects.filter(contentId=contentid)
    # pprint.pprint(commons)
    serializer = SearchByContentIdSerializer(commons, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def detailserializers(request):
    '''
    상세정보 출력
    '''
    details = Detail.objects.all()
    serializer = DetailSerializer(details, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def scoreserailizers(request):
    '''
    score 전체정보 출력
    '''
    scores = Score.objects.all()
    serailizer = ScoreSerailizer(scores, many=True)
    return Response(serailizer.data)


# api db 저장 및 update
def detailcommon(request):
    # ServiceKey = "tG2pbhauvACu6IO20lRl4NIY5qDcRrFnl21s57G6XgwovyquyiFquhZgoE%2FBmG930wyBEyxx4pNZEyxzt8%2Brvg%3D%3D"
    # ServiceKey = "5Z64FYjCYoIRrToMriTzGi%2BbzlzcHOFJKdG9NFgR77i52r%2BCCi6XbU9gpq15l8fEGojdilIdq0iyzQvIpe3BlQ%3D%3D"
    # ServiceKey = "6cNC8ZB6rpRzhoiI%2B34pu9noit6ISM6GZIK52Zl3cA0NZ5unLdnyGwdPypDhk%2BRc11nFW4y8C%2FFCsT%2BNR9hTOg%3D%3D"
    # ServiceKey = "dFPOj2N3FaviYly9Z3wC7C2hpqBqatZHRJ%2F0pVADU781L%2FQ8YwR9AZTEIwS8zMhq6ale2Ua1SbaqEKKff1u2Gg%3D%3D"
    ServiceKey = "jOHhL9XBFjNJN5zQeQnKKKuwBUcaCUsq4eZadEhdbBZ3dmgnYBjpyCKkLixpqIRUvbkT1RHNr3UPSB%2Fwwx29%2BQ%3D%3D"
    url = "http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList?ServiceKey="
    option = "&contentTypeId=&defaultYN=Y&overviewYN=Y&addrinfoYN=Y&areacodeYN=Y&sigungucodeYN=Y&numOfRows=25344&pageNo=1&MobileOS=AND&MobileApp=travel5&_type=json"
    url_ = url + ServiceKey + option

    request_ = urllib.request.Request(url_)
    response = urllib.request.urlopen(request_)
    rescode = response.getcode()
    print(rescode)

    if (rescode == 200):
        column_list = ['contentId', 'category', 'tel', 'addr1', 'addr2', 'area', 'sigungu', 'title', 'overview',
                       'zipCode', 'homepage', 'mapx', 'mapy']
        items_list = ['contentid', 'contenttypeid', 'tel', 'addr1', 'addr2', 'areacode', 'sigungucode', 'title',
                      'overview', 'zipcode', 'homepage', 'mapx', 'mapy']
        response_body = response.read()
        dict = json.loads(response_body.decode('utf-8'))
        items = dict['response']['body']['items']['item']

        for item in items:
            result_value = []
            result_column = []
            for i in items_list:
                if i in item.keys():
                    result_value.append(item[i])
                    result_column.append(column_list[items_list.index(i)])
                else:
                    if items_list.index(i) in [0, 1, 5, 6, 11, 12]:
                        result_value.append(0)
                    else:
                        result_value.append('없음')
                    result_column.append(column_list[items_list.index(i)])
            # print(int(result_value[0]))
            # print(result_value)

            if int(result_value[1]) == 25:
                continue

            if (Common.objects.filter(contentId=int(result_value[0])).exists()):
                print('지금 있대!')
                common = Common.objects.filter(contentId=int(result_value[0]))
                # print(common.first().tel)

                common = common.first().update(tel=result_value[2], addr1=result_value[3], addr2=result_value[4],
                                               area=int(result_value[5]), sigungu=int(result_value[6]),
                                               title=result_value[7],
                                               overview=result_value[8], zipCode=result_value[9],
                                               homepage=result_value[10],
                                               mapx=float(result_value[11]), mapy=float(result_value[12]))
                common.save()
                print(common.pk, 'common save')
            else:
                print('없어서 만든대!')
                common = Common(contentId=int(result_value[0]), category=int(result_value[1]), tel=result_value[2],
                                addr1=result_value[3], addr2=result_value[4], area=int(result_value[5]),
                                sigungu=int(result_value[6]), title=result_value[7], overview=result_value[8],
                                zipCode=result_value[9], homepage=result_value[10],
                                mapx=float(result_value[11]), mapy=float(result_value[12]))
                common.save()
                print(common.pk, 'common save')


    else:
        print("잠시 후에 다시 도전!")

    return redirect(reverse('maps:main'))


# homepage html형식 변경해서 저장하기
## homepage 형태 :
#           1) 이름 <a href >www.sd.com</a>
#           2) www.djk.com
#           3) 없음
## overview 형태 : 1) <strong /> 2) text
## image 형태 : list => 1) ["null"] 2) ["img1.url", "img2.url"]
def detaildetail(request):
    commons = Common.objects.all()

    for test in commons:
        common = Common.objects.get(contentId=test.contentId)
        detail_content_id = test.contentId
        print('id', detail_content_id)

        if common.homepage != "없음":
            continue
        else:
            ##### image 저장 #####
            print('image start')
            # detail_key = "tG2pbhauvACu6IO20lRl4NIY5qDcRrFnl21s57G6XgwovyquyiFquhZgoE%2FBmG930wyBEyxx4pNZEyxzt8%2Brvg%3D%3D"
            detail_key = "5Z64FYjCYoIRrToMriTzGi%2BbzlzcHOFJKdG9NFgR77i52r%2BCCi6XbU9gpq15l8fEGojdilIdq0iyzQvIpe3BlQ%3D%3D"
            # detail_key = "6cNC8ZB6rpRzhoiI%2B34pu9noit6ISM6GZIK52Zl3cA0NZ5unLdnyGwdPypDhk%2BRc11nFW4y8C%2FFCsT%2BNR9hTOg%3D%3D"
            # detail_key = "dFPOj2N3FaviYly9Z3wC7C2hpqBqatZHRJ%2F0pVADU781L%2FQ8YwR9AZTEIwS8zMhq6ale2Ua1SbaqEKKff1u2Gg%3D%3D"
            # detail_key = "jOHhL9XBFjNJN5zQeQnKKKuwBUcaCUsq4eZadEhdbBZ3dmgnYBjpyCKkLixpqIRUvbkT1RHNr3UPSB%2Fwwx29%2BQ%3D%3D"
            # detail_key = "rbssLvuPaumnRlgRCPsgU5IeLlHAf5nHHGU8P3JVSYqJvgSFL8l%2FJbCYNE9zVd5Je%2BFoFlSBFo%2Fochd7h97a%2Fg%3D%3D" #종찬씨 key(가급적 사용 x)
            image_url = f"http://api.visitkorea.or.kr/openapi/service/rest/KorService/detailImage?ServiceKey={detail_key}&contentId={detail_content_id}&imageYN=Y&MobileOS=ETC&MobileApp=AppTest&_type=json"
            temp_url = urllib.request.urlopen(image_url)
            f = temp_url.read()
            content = json.loads(f.decode('utf-8'))
            # pprint.pprint(content)
            image_items = content['response']['body']['items']

            image_list = []
            if image_items == '':
                image_list.append("null")
            else:
                for item in image_items['item']:
                    if type({'key': '1'}) == type(item):
                        image_list.append(item['originimgurl'])
                    else:
                        image_list.append(image_items['item']['originimgurl'])

            common.image = image_list
            common.save()
            print('image save')

            print('overview/homepage start')
            # overview
            detailinfo_url = f"http://api.visitkorea.or.kr/openapi/service/rest/KorService/detailCommon?ServiceKey={detail_key}&contentId={detail_content_id}&defaultYN=Y&overviewYN=Y&MobileOS=ETC&MobileApp=AppTest&_type=json"
            temp_url = urllib.request.urlopen(detailinfo_url)
            f = temp_url.read()
            content = json.loads(f.decode('utf-8'))
            # pprint.pprint(content)

            detail_items = content['response']['body']['items']['item']

            if 'homepage' in detail_items.keys():
                homepy = detail_items['homepage']
                common.homepage = homepy
            if 'overview' in detail_items.keys():
                infotext = detail_items['overview']
                common.overview = infotext
            common.save()
            print('over/home save')

    return redirect(reverse('maps:main'))


def detailcontent(request):
    commons = Common.objects.all()
    # print(len(commons))

    for test in commons:
        common = Common.objects.get(contentId=test.contentId)
        detail_content_id = test.contentId
        detail_content_type = test.category
        print('id', detail_content_id)
        print('type', detail_content_type)

        if (Detail.objects.filter(detailId=detail_content_id).exists()):
            # detail = Detail.objects.get(detailId=detail_content_id)
            # print(detail)
            continue
        else:
            print('detail start')
            # detail 저장
            # detail_key = "tG2pbhauvACu6IO20lRl4NIY5qDcRrFnl21s57G6XgwovyquyiFquhZgoE%2FBmG930wyBEyxx4pNZEyxzt8%2Brvg%3D%3D"
            # detail_key = "5Z64FYjCYoIRrToMriTzGi%2BbzlzcHOFJKdG9NFgR77i52r%2BCCi6XbU9gpq15l8fEGojdilIdq0iyzQvIpe3BlQ%3D%3D"
            # detail_key = "6cNC8ZB6rpRzhoiI%2B34pu9noit6ISM6GZIK52Zl3cA0NZ5unLdnyGwdPypDhk%2BRc11nFW4y8C%2FFCsT%2BNR9hTOg%3D%3D"
            detail_key = "dFPOj2N3FaviYly9Z3wC7C2hpqBqatZHRJ%2F0pVADU781L%2FQ8YwR9AZTEIwS8zMhq6ale2Ua1SbaqEKKff1u2Gg%3D%3D"
            # detail_key = "jOHhL9XBFjNJN5zQeQnKKKuwBUcaCUsq4eZadEhdbBZ3dmgnYBjpyCKkLixpqIRUvbkT1RHNr3UPSB%2Fwwx29%2BQ%3D%3D"
            # detail_key = "rbssLvuPaumnRlgRCPsgU5IeLlHAf5nHHGU8P3JVSYqJvgSFL8l%2FJbCYNE9zVd5Je%2BFoFlSBFo%2Fochd7h97a%2Fg%3D%3D"
            detailintro_url = f"http://api.visitkorea.or.kr/openapi/service/rest/KorService/detailIntro?ServiceKey={detail_key}&contentId={detail_content_id}&contentTypeId={detail_content_type}&MobileOS=ETC&MobileApp=AppTest&_type=json&numOfRows="
            temp_url = urllib.request.urlopen(detailintro_url)
            f = temp_url.read()
            content = json.loads(f.decode('utf-8'))
            # pprint.pprint(content)
            if 'body' not in content['response']:
                print('Limit Number of Service Key!!!!')
                print(len(Detail.objects.all()))
                break
            else:
                detail_items = content['response']['body']['items']['item']

        detail_sets = ['startTime', 'endTime', 'parking', 'chkPet', 'chkBaby', 'restDate',
                       'useTime', 'ageLimit', 'pay', 'barbeque', 'refund', 'subevent',
                       'openPeriod', 'discountInfo', 'chkCook', 'openTime', 'chkPack',
                       'chkSmoking', 'infoCenter', ]
        detail_value = []

        # 관광지
        if detail_content_type == 12:
            print('typein')
            detail_set = {
                'chkBaby': 'chkbabycarriage',
                'chkPet': 'chkpet',
                'ageLimit': 'expagerange',
                'restDate': 'restdate',
                'useTime': 'usetime'
            }

            for i in detail_sets:
                if i in detail_set.keys() and detail_set[i] in detail_items.keys():
                    detail_value.append(detail_items[detail_set[i]])
                else:
                    detail_value.append('정보 없음')

            # if flag == 0 :
            #     detail = Detail.objects.filter(detailId=detail_content_id).first()
            #     detail.update(startTime=detail_value[0], endTime=detail_value[1], parking=detail_value[2], chkPet=detail_value[3],
            #             chkBaby=detail_value[4], restDate=detail_value[5], useTime=detail_value[6], ageLimit=detail_value[7],
            #             pay=detail_value[8], barbeque=detail_value[9], refund=detail_value[10], subevent=detail_value[11],
            #             openPeriod=detail_value[12], discountInfo=detail_value[13], chkCook=detail_value[14], openTime=detail_value[15],
            #             chkPack=detail_value[16], chkSmoking=detail_value[17], infoCenter=detail_value[18])
            # detail.save()
            # else:

            detail = Detail(detailId=int(detail_content_id), startTime=detail_value[0], endTime=detail_value[1],
                            parking=detail_value[2], chkPet=detail_value[3],
                            chkBaby=detail_value[4], restDate=detail_value[5], useTime=detail_value[6],
                            ageLimit=detail_value[7],
                            pay=detail_value[8], barbeque=detail_value[9], refund=detail_value[10],
                            subevent=detail_value[11],
                            openPeriod=detail_value[12], discountInfo=detail_value[13], chkCook=detail_value[14],
                            openTime=detail_value[15],
                            chkPack=detail_value[16], chkSmoking=detail_value[17], infoCenter=detail_value[18])

            detail.common = common
            detail.save()

        # 행사/공연/축제
        if detail_content_type == 15:
            detail_set = {
                'ageLimit': 'agelimit',
                'startTime': 'eventstartdate',
                'endTime': 'eventenddate',
                'subevent': 'subevent'
            }

            for i in detail_sets:
                if i in detail_set.keys() and detail_set[i] in detail_items.keys():
                    # detail = Detail.objects.get(detailId=detail_pk)
                    # print(detail)
                    detail_value.append(detail_items[detail_set[i]])
                else:
                    detail_value.append('정보 없음')
            # print(detail_value)

            detail = Detail(detailId=int(detail_content_id), startTime=detail_value[0], endTime=detail_value[1],
                            parking=detail_value[2], chkPet=detail_value[3],
                            chkBaby=detail_value[4], restDate=detail_value[5], useTime=detail_value[6],
                            ageLimit=detail_value[7],
                            pay=detail_value[8], barbeque=detail_value[9], refund=detail_value[10],
                            subevent=detail_value[11],
                            openPeriod=detail_value[12], discountInfo=detail_value[13], chkCook=detail_value[14],
                            openTime=detail_value[15],
                            chkPack=detail_value[16], chkSmoking=detail_value[17], infoCenter=detail_value[18])

            detail.common = common
            detail.save()

        # 문화시설
        if detail_content_type == 14:
            detail_set = {
                'chkBaby': 'chkbabycarriageculture',
                'chkPet': 'chkpetculture',
                'discountInfo': 'discountinfo',
                'pay': 'usefee'
            }

            for i in detail_sets:
                if i in detail_set.keys() and detail_set[i] in detail_items.keys():
                    # detail = Detail.objects.get(detailId=detail_pk)
                    # print(detail)
                    detail_value.append(detail_items[detail_set[i]])
                else:
                    detail_value.append('정보 없음')
            # print(detail_value)

            detail = Detail(detailId=int(detail_content_id), startTime=detail_value[0], endTime=detail_value[1],
                            parking=detail_value[2], chkPet=detail_value[3],
                            chkBaby=detail_value[4], restDate=detail_value[5], useTime=detail_value[6],
                            ageLimit=detail_value[7],
                            pay=detail_value[8], barbeque=detail_value[9], refund=detail_value[10],
                            subevent=detail_value[11],
                            openPeriod=detail_value[12], discountInfo=detail_value[13], chkCook=detail_value[14],
                            openTime=detail_value[15],
                            chkPack=detail_value[16], chkSmoking=detail_value[17], infoCenter=detail_value[18])

            detail.common = common
            detail.save()

        # 레포츠
        if detail_content_type == 28:
            detail_set = {
                'chkBaby': 'chkbabycarriageleports',
                'chkPet': 'chkpetleports',
                'ageLimit': 'agelimit',
                'openPeriod': 'openperiod',
                'pay': 'usefeeleports'
            }

            for i in detail_sets:
                if i in detail_set.keys() and detail_set[i] in detail_items.keys():
                    # detail = Detail.objects.get(detailId=detail_pk)
                    # print(detail)
                    detail_value.append(detail_items[detail_set[i]])
                else:
                    detail_value.append('정보 없음')
            # print(detail_value)

            detail = Detail(detailId=int(detail_content_id), startTime=detail_value[0], endTime=detail_value[1],
                            parking=detail_value[2], chkPet=detail_value[3],
                            chkBaby=detail_value[4], restDate=detail_value[5], useTime=detail_value[6],
                            ageLimit=detail_value[7],
                            pay=detail_value[8], barbeque=detail_value[9], refund=detail_value[10],
                            subevent=detail_value[11],
                            openPeriod=detail_value[12], discountInfo=detail_value[13], chkCook=detail_value[14],
                            openTime=detail_value[15],
                            chkPack=detail_value[16], chkSmoking=detail_value[17], infoCenter=detail_value[18])

            detail.common = common
            detail.save()

        # 숙박
        if detail_content_type == 32:
            detail_set = {
                'chkinTime': 'checkintime',
                'chkoutTime': 'checkouttime',
                'chkCook': 'chkcooking',
                'subevent': 'subfacility',
                'refund': 'refundrequlation'
            }

            for i in detail_sets:
                if i in detail_set.keys() and detail_set[i] in detail_items.keys():
                    # detail = Detail.objects.get(detailId=detail_pk)
                    # print(detail)
                    detail_value.append(detail_items[detail_set[i]])
                else:
                    detail_value.append('정보 없음')
            # print(detail_value)

            detail = Detail(detailId=int(detail_content_id), startTime=detail_value[0], endTime=detail_value[1],
                            parking=detail_value[2], chkPet=detail_value[3],
                            chkBaby=detail_value[4], restDate=detail_value[5], useTime=detail_value[6],
                            ageLimit=detail_value[7],
                            pay=detail_value[8], barbeque=detail_value[9], refund=detail_value[10],
                            subevent=detail_value[11],
                            openPeriod=detail_value[12], discountInfo=detail_value[13], chkCook=detail_value[14],
                            openTime=detail_value[15],
                            chkPack=detail_value[16], chkSmoking=detail_value[17], infoCenter=detail_value[18])

            detail.common = common
            detail.save()

        # 쇼핑
        if detail_content_type == 38:
            detail_set = {
                'chkBaby': 'chkbabycarriageshopping',
                'chkPet': 'chkpetshopping',
                'openPeriod': 'chkcooking',
                'subevent': 'opendateshopping',
                'openTime': 'opentime'
            }
            for i in detail_sets:
                if i in detail_set.keys() and detail_set[i] in detail_items.keys():
                    # detail = Detail.objects.get(detailId=detail_pk)
                    # print(detail)
                    detail_value.append(detail_items[detail_set[i]])
                else:
                    detail_value.append('정보 없음')
            # print(detail_value)

            detail = Detail(detailId=int(detail_content_id), startTime=detail_value[0], endTime=detail_value[1],
                            parking=detail_value[2], chkPet=detail_value[3],
                            chkBaby=detail_value[4], restDate=detail_value[5], useTime=detail_value[6],
                            ageLimit=detail_value[7],
                            pay=detail_value[8], barbeque=detail_value[9], refund=detail_value[10],
                            subevent=detail_value[11],
                            openPeriod=detail_value[12], discountInfo=detail_value[13], chkCook=detail_value[14],
                            openTime=detail_value[15],
                            chkPack=detail_value[16], chkSmoking=detail_value[17], infoCenter=detail_value[18])

            detail.common = common
            detail.save()

        # 음식점
        if detail_content_type == 39:
            detail_set = {
                'discountInfo': 'discountinfofood',
                'chkBaby': 'kidsfacility',
                'chkPack': 'packing',
                'chkSmoking': 'smoking',
                'openTime': 'opentimefood'
            }

            for i in detail_sets:
                if i in detail_set.keys() and detail_set[i] in detail_items.keys():
                    # detail = Detail.objects.get(detailId=detail_pk)
                    # print(detail)
                    detail_value.append(detail_items[detail_set[i]])
                else:
                    detail_value.append('정보 없음')
            # print(detail_value)

            detail = Detail(detailId=int(detail_content_id), startTime=detail_value[0], endTime=detail_value[1],
                            parking=detail_value[2], chkPet=detail_value[3],
                            chkBaby=detail_value[4], restDate=detail_value[5], useTime=detail_value[6],
                            ageLimit=detail_value[7],
                            pay=detail_value[8], barbeque=detail_value[9], refund=detail_value[10],
                            subevent=detail_value[11],
                            openPeriod=detail_value[12], discountInfo=detail_value[13], chkCook=detail_value[14],
                            openTime=detail_value[15],
                            chkPack=detail_value[16], chkSmoking=detail_value[17], infoCenter=detail_value[18])

            detail.common = common
            detail.save()
        print('detail save')

    return redirect(reverse('maps:main'))
