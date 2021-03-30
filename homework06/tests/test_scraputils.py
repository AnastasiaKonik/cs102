import pytest
import requests
from bs4 import BeautifulSoup

import scraputils
from scraputils import extract_news


def test_extract_news() -> None:
    test_page = """<html lang="en" op="newest">
<head>
    <meta name="referrer" content="origin">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="news.css?JdopuflobkJrURh551j6">
    <link rel="shortcut icon" href="favicon.ico">
    <title>New Links | Hacker News</title></head>
<body>
<center>
    <table id="hnmain" border="0" cellpadding="0" cellspacing="0" width="85%" bgcolor="#f6f6ef">
        <tr>
            <td bgcolor="#ff6600">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="padding:2px">
                    <tr>
                        <td style="width:18px;padding-right:4px"><a href="https://news.ycombinator.com"><img
                                src="y18.gif" width="18" height="18" style="border:1px white solid;"></a></td>
                        <td style="line-height:12pt; height:10px;"><span class="pagetop"><b class="hnname"><a
                                href="news">Hacker News</a></b>
              <span class="topsel"><a href="newest">new</a></span> | <a href="front">past</a> | <a href="newcomments">comments</a> | <a
                                    href="ask">ask</a> | <a href="show">show</a> | <a href="jobs">jobs</a> | <a
                                    href="submit">submit</a>            </span></td>
                        <td style="text-align:right;padding-right:4px;"><span class="pagetop">
                              <a href="login?goto=newest">login</a>
                          </span></td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr id="pagespace" title="New Links" style="height:10px"></tr>
        <tr>
            <td>
                <table border="0" cellpadding="0" cellspacing="0" class="itemlist">
                    <tr class='athing' id='26601334'>
                        <td align="right" valign="top" class="title"><span class="rank">1.</span></td>
                        <td valign="top" class="votelinks">
                            <center><a id='up_26601334' href='vote?id=26601334&amp;how=up&amp;goto=newest'>
                                <div class='votearrow' title='upvote'></div>
                            </a></center>
                        </td>
                        <td class="title"><a
                                href="https://publicdomainreview.org/collection/catalogue-of-the-68-competitive-designs-for-the-great-tower-for-london-1890"
                                class="storylink" rel="nofollow">Catalogue of the 68 competitive designs for the great
                            tower for London (1890)</a><span class="sitebit comhead"> (<a
                                href="from?site=publicdomainreview.org"><span
                                class="sitestr">publicdomainreview.org</span></a>)</span></td>
                    </tr>
                    <tr>
                        <td colspan="2"></td>
                        <td class="subtext">
                            <span class="score" id="score_26601334">1 point</span> by <a href="user?id=BerislavLopac"
                                                                                         class="hnuser">BerislavLopac</a>
                            <span class="age"><a href="item?id=26601334">5 minutes ago</a></span> <span
                                id="unv_26601334"></span> | <a href="hide?id=26601334&amp;goto=newest">hide</a> | <a
                                href="https://hn.algolia.com/?query=Catalogue%20of%20the%2068%20competitive%20designs%20for%20the%20great%20tower%20for%20London&type=story&dateRange=all&sort=byDate&storyText=false&prefix&page=0"
                                class="hnpast">past</a> | <a href="item?id=26601334">discuss</a></td>
                    </tr>
                    <tr class="spacer" style="height:5px"></tr>
                    <tr class='athing' id='26601318'>
                        <td align="right" valign="top" class="title"><span class="rank">2.</span></td>
                        <td valign="top" class="votelinks">
                            <center><a id='up_26601318' href='vote?id=26601318&amp;how=up&amp;goto=newest'>
                                <div class='votearrow' title='upvote'></div>
                            </a></center>
                        </td>
                        <td class="title"><a
                                href="https://www.theguardian.com/money/shortcuts/2021/mar/22/make-mine-a-micro-job-why-working-one-day-a-week-is-the-secret-of-happiness"
                                class="storylink" rel="nofollow">Make mine a micro-job Why working one day a week is the
                            secret of happiness</a><span class="sitebit comhead"> (<a
                                href="from?site=theguardian.com"><span
                                class="sitestr">theguardian.com</span></a>)</span></td>
                    </tr>
                    <tr>
                        <td colspan="2"></td>
                        <td class="subtext">
                            <span class="score" id="score_26601318">1 point</span> by <a href="user?id=tonyedgecombe"
                                                                                         class="hnuser">tonyedgecombe</a>
                            <span class="age"><a href="item?id=26601318">10 minutes ago</a></span> <span
                                id="unv_26601318"></span> | <a href="hide?id=26601318&amp;goto=newest">hide</a> | <a
                                href="https://hn.algolia.com/?query=Make%20mine%20a%20micro-job%20Why%20working%20one%20day%20a%20week%20is%20the%20secret%20of%20happiness&type=story&dateRange=all&sort=byDate&storyText=false&prefix&page=0"
                                class="hnpast">past</a> | <a href="item?id=26601318">discuss</a></td>
                    </tr>
                    <tr class="spacer" style="height:5px"></tr>
                    <tr class='athing' id='26601290'>
                        <td align="right" valign="top" class="title"><span class="rank">3.</span></td>
                        <td valign="top" class="votelinks">
                            <center><a id='up_26601290' href='vote?id=26601290&amp;how=up&amp;goto=newest'>
                                <div class='votearrow' title='upvote'></div>
                            </a></center>
                        </td>
                        <td class="title"><a
                                href="https://www.data-show.com/blog/2020-world-press-freedom-index-a-decisive-decade-for-the-future-of-journalism/"
                                class="storylink" rel="nofollow">2020 World Press Freedom Index: A decisive decade for
                            the future of journalism</a><span class="sitebit comhead"> (<a
                                href="from?site=data-show.com"><span class="sitestr">data-show.com</span></a>)</span>
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2"></td>
                        <td class="subtext">
                            <span class="score" id="score_26601290">2 points</span> by <a href="user?id=emmanuelgautier"
                                                                                          class="hnuser">emmanuelgautier</a>
                            <span class="age"><a href="item?id=26601290">19 minutes ago</a></span> <span
                                id="unv_26601290"></span> | <a href="hide?id=26601290&amp;goto=newest">hide</a> | <a
                                href="https://hn.algolia.com/?query=2020%20World%20Press%20Freedom%20Index%3A%20A%20decisive%20decade%20for%20the%20future%20of%20journalism&type=story&dateRange=all&sort=byDate&storyText=false&prefix&page=0"
                                class="hnpast">past</a> | <a href="item?id=26601290">discuss</a></td>
                    </tr>
                    <tr class="spacer" style="height:5px"></tr>
                    <tr class='athing' id='26601278'>
                        <td align="right" valign="top" class="title"><span class="rank">4.</span></td>
                        <td valign="top" class="votelinks">
                            <center><a id='up_26601278' href='vote?id=26601278&amp;how=up&amp;goto=newest'>
                                <div class='votearrow' title='upvote'></div>
                            </a></center>
                        </td>
                        <td class="title"><a
                                href="https://phys.org/news/2021-03-huge-uptick-lightning-arctic-decade.html"
                                class="storylink" rel="nofollow">Uptick in lightning over the Arctic in past
                            decade</a><span class="sitebit comhead"> (<a href="from?site=phys.org"><span
                                class="sitestr">phys.org</span></a>)</span></td>
                    </tr>
                    <tr>
                        <td colspan="2"></td>
                        <td class="subtext">
                            <span class="score" id="score_26601278">1 point</span> by <a href="user?id=dnetesn"
                                                                                         class="hnuser">dnetesn</a>
                            <span class="age"><a href="item?id=26601278">22 minutes ago</a></span> <span
                                id="unv_26601278"></span> | <a href="hide?id=26601278&amp;goto=newest">hide</a> | <a
                                href="https://hn.algolia.com/?query=Uptick%20in%20lightning%20over%20the%20Arctic%20in%20past%20decade&type=story&dateRange=all&sort=byDate&storyText=false&prefix&page=0"
                                class="hnpast">past</a> | <a href="item?id=26601278">discuss</a></td>
                    </tr>
                    <tr class="spacer" style="height:5px"></tr>
                    <tr class='athing' id='26601275'>
                        <td align="right" valign="top" class="title"><span class="rank">5.</span></td>
                        <td valign="top" class="votelinks">
                            <center><a id='up_26601275' href='vote?id=26601275&amp;how=up&amp;goto=newest'>
                                <div class='votearrow' title='upvote'></div>
                            </a></center>
                        </td>
                        <td class="title"><a href="https://academictimes.com/elite-philanthropy-mainly-self-serving-2/"
                                             class="storylink" rel="nofollow">Elite philanthropy mainly self-serving</a><span
                                class="sitebit comhead"> (<a href="from?site=academictimes.com"><span class="sitestr">academictimes.com</span></a>)</span>
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2"></td>
                        <td class="subtext">
                            <span class="score" id="score_26601275">1 point</span> by <a href="user?id=rytis"
                                                                                         class="hnuser">rytis</a> <span
                                class="age"><a href="item?id=26601275">23 minutes ago</a></span> <span
                                id="unv_26601275"></span> | <a href="hide?id=26601275&amp;goto=newest">hide</a> | <a
                                href="https://hn.algolia.com/?query=Elite%20philanthropy%20mainly%20self-serving&type=story&dateRange=all&sort=byDate&storyText=false&prefix&page=0"
                                class="hnpast">past</a> | <a href="item?id=26601275">discuss</a></td>
                    </tr>
                    <tr class="spacer" style="height:5px"></tr>
                </table>
            </td>
        </tr>
    </table>
</center>
</body>
</html>
"""
    soup = BeautifulSoup(test_page, "html.parser")
    assert extract_news(soup) == [
        {
            "author": "BerislavLopac",
            "points": 1,
            "title": "Catalogue of the 68 competitive designs for the great\n                            tower for London (1890)",
            "url": "https://publicdomainreview.org/collection/catalogue-of-the-68-competitive-designs-for-the-great-tower-for-london-1890",
        },
        {
            "author": "tonyedgecombe",
            "points": 1,
            "title": "Make mine a micro-job Why working one day a week is the\n                            secret of happiness",
            "url": "https://www.theguardian.com/money/shortcuts/2021/mar/22/make-mine-a-micro-job-why-working-one-day-a-week-is-the-secret-of-happiness",
        },
        {
            "author": "emmanuelgautier",
            "points": 2,
            "title": "2020 World Press Freedom Index: A decisive decade for\n                            the future of journalism",
            "url": "https://www.data-show.com/blog/2020-world-press-freedom-index-a-decisive-decade-for-the-future-of-journalism/",
        },
        {
            "author": "dnetesn",
            "points": 1,
            "title": "Uptick in lightning over the Arctic in past\n                            decade",
            "url": "https://phys.org/news/2021-03-huge-uptick-lightning-arctic-decade.html",
        },
        {
            "author": "rytis",
            "points": 1,
            "title": "Elite philanthropy mainly self-serving",
            "url": "https://academictimes.com/elite-philanthropy-mainly-self-serving-2/",
        },
    ]


def test_extract_next_page() -> None:
    url = "https://news.ycombinator.com/"
    for i in range(2, 7):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        next_url = scraputils.extract_next_page(soup)
        assert next_url == "news?p=" + str(i)
        url = "https://news.ycombinator.com/" + next_url


def test_get_news() -> None:
    url = "https://news.ycombinator.com/newest"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    news_list = extract_news(soup)
    assert news_list
