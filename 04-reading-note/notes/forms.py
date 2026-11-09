from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Book, Note

MAX_COVER_SIZE = 2 * 1024 * 1024  # 표지는 2MB까지
RATING_CHOICES = [("", "별점 없음")] + [(n, "★" * n) for n in range(1, 6)]


class BookForm(forms.ModelForm):
    rating = forms.TypedChoiceField(
        label="별점", choices=RATING_CHOICES, coerce=int, empty_value=None, required=False
    )

    class Meta:
        model = Book
        fields = ["title", "author", "status", "rating", "finished_on", "cover"]
        widgets = {"finished_on": forms.DateInput(attrs={"type": "date"})}

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating is not None and not 1 <= rating <= 5:
            raise forms.ValidationError("별점은 1점부터 5점까지 고를 수 있습니다.")
        return rating

    def clean_finished_on(self):
        finished_on = self.cleaned_data.get("finished_on")
        if finished_on and finished_on > date.today():
            raise forms.ValidationError("다 읽은 날은 오늘보다 뒤일 수 없습니다.")
        return finished_on

    def clean_cover(self):
        cover = self.cleaned_data.get("cover")
        if cover and hasattr(cover, "size") and cover.size > MAX_COVER_SIZE:
            raise forms.ValidationError("표지 사진은 2MB까지 올릴 수 있습니다.")
        return cover

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("finished_on") and cleaned.get("status") != Book.Status.DONE:
            self.add_error("status", "다 읽은 날을 적으려면 읽는 상태를 '다 읽음'으로 고르세요.")
        return cleaned


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["body"]
        labels = {"body": "새 메모"}
        widgets = {"body": forms.Textarea(attrs={"rows": 3, "placeholder": "읽으며 든 생각을 적어 보세요."})}


class SignUpForm(UserCreationForm):
    pass
