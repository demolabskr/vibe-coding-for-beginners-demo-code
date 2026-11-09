from django.shortcuts import render


def home(request):
    # 아직 데이터베이스가 없으므로 책 세 권을 코드에 적어 보여 준다.
    books = [
        {"title": "아몬드", "author": "손원평", "status": "다 읽음"},
        {"title": "데미안", "author": "헤르만 헤세", "status": "읽는 중"},
        {"title": "채식주의자", "author": "한강", "status": "읽고 싶음"},
    ]
    return render(request, "notes/home.html", {"books": books})


def about(request):
    return render(request, "notes/about.html")
