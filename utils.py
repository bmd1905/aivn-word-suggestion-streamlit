import streamlit as st
from htbuilder import HtmlElement, div, br, hr, a, p, img, styles
from htbuilder.units import percent, px



def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        image('https://scontent-ams2-1.xx.fbcdn.net/v/t39.30808-6/326762542_533351005436945_3355631653176967012_n.png?_nc_cat=1&ccb=1-7&_nc_sid=5f2048&_nc_ohc=J2pKQDyGdRgAX_FLksV&_nc_ht=scontent-ams2-1.xx&oh=00_AfDN3M3ADdj9HUK4qGIkj-F77QU6P5hja1XkdcjQQtUg2w&oe=6563863F',
              width=px(75), height=px(75)),
        br(),
        "Made by ",
        link("https://www.facebook.com/aivietnam.edu.vn", "AI VIETNAM"),
    ]
    layout(*myargs)