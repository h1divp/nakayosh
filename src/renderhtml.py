import random

class Renderer():
    def __init__(self, data: [tuple]):
        self.data = data
        self.player_colors = dict()

    def viewhist(self):
        print(self.data)
        print(self.player_colors)

    def gencolor(self):
        def r(): return random.randint(0,200) # I don't want the colors too bright
        return f"#{r():02x}{r():02x}{r():02x}"
        
    def genplayercolors(self):
        for x in self.data:
            if x[0] != "" and self.player_colors.get(x[0]) is None:
                self.player_colors[x[0]] = self.gencolor()
        
    def generatehtml(self):
        HTML_HEADER = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8" />
          <title>shiritori</title>
          <meta name="viewport" content="width=device-width,initial-scale=1" />
          <style type="text/css">
            @page {
              size: landscape;
              margin: 2px 0.2in;
              height: 0.5in;
            }
            body {
                font-family: "Noto Sans Japanese"
            }
            span {
              margin: 1vh 0;
            }
            .container {
              display: flex;
              flex-flow: row wrap;
              align-items: center;
              justify-content: center;
              font-size: 2rem;
            }
            .header {
              display: flex;
              flex-flow: row wrap;
              align-items: center;
              justify-content: space-around;
              font-size: 1.5rem;
            }
          </style>
        </head>
        <body>
        """.strip()

        HTML_FOOTER = """
            </div>
        </body>
        </html>
        """.strip()

        self.genplayercolors()

        result_html = ""
        result_html += f"{HTML_HEADER}"
        result_html += "<div class=\"header\">"
        for x in self.player_colors:
            result_html += f"<span style=\"color:{self.player_colors.get(x)}\">{x} </span>"
        result_html += "</div>"

        result_html += "<div class=\"container\">"
        # tuples are in form (author, word, feature)
        for x in self.data:
            if x[2] != "wrong":
                word = f"<span style=\"color:{self.player_colors.get(x[0])}\">" + x[1] + "</span>"
                result_html += word
            else: 
                word = f"<span style=\"color:{self.player_colors.get(x[0])};text-decoration:line-through;\">" + x[1] + "</span>"
                result_html += word

            result_html += "<span>"
            if x[2] == "correct":
                result_html += "→"
            if x[2] == "wrong":
                result_html += "　"
            elif x[2] == "end":
                result_html += "☓ "
            elif x[2] == "continuing":
                result_html += "…"
            result_html += "</span>"
        result_html += "</span>"
        result_html += f"{HTML_FOOTER}"
        return result_html

    def render(self, fileName):
        with open(fileName, 'w', encoding='utf-8') as fileOut:
            generated_html = self.generatehtml()
            fileOut.write(generated_html)
  

