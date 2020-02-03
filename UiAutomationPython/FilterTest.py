#!/usr/bin/env python3
import pytest
import Pages


@pytest.mark.usefixtures("driver")
class TestFilter:
    def test_filter_by_year(self):
        home_page = Pages.Homepage(self.driver)
        home_page.navigate()
        home_page.click_on_filter_button()
        home_page.filter_by_year("year2017")
        articles, first_article_name = home_page.get_first_article_name()
        assert len(articles) > 1
        home_page.click_on_reset_button()
        articles_without_filter, first_article_name_without_filter = home_page.get_first_article_name()
        assert len(articles_without_filter) > 1
        assert first_article_name != first_article_name_without_filter
