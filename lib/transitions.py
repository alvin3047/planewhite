from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.app import App
from kivy.graphics import RenderContext
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.core.window import Window

alpha_fragment = '''
#ifdef GL_ES
    precision highp float;
#endif

/* Outputs from the vertex shader */
varying vec4 frag_color;
varying vec2 tex_coord0;

/* uniform texture samplers */
uniform sampler2D texture0;

/* our custom alpha value */
uniform float alpha;

void main (void){
    vec4 alpha_color = vec4(1, 1, 1, alpha);
    gl_FragColor = alpha_color * frag_color * texture2D(texture0, tex_coord0);
}
'''


class AlphaScatter(Scatter):
    alpha = NumericProperty(1.)

    def __init__(self, **kwargs):
        self.canvas = RenderContext()
        self.canvas.shader.fs = alpha_fragment
        super(AlphaScatter, self).__init__(**kwargs)
        Clock.schedule_once(self.init_shader, 0)

    def init_shader(self, dt):
        self.canvas['projection_mat'] = Window.render_context['projection_mat']

    def on_alpha(self, instance, value):
        self.canvas['alpha'] = value


class ShaderAlphaApp(App):
    def build(self):
        size = (300, 300)
        scatter = AlphaScatter(size_hint=(None, None), size=size)
        layout = GridLayout(size=size, cols=2, padding=50)
        for x in xrange(4):
            layout.add_widget(Button(text=str(x)))
        scatter.add_widget(layout)

        # a little clock to change the alpha of the scatter 
        Clock.schedule_interval(self.change_scatter_alpha, 1 / 30)
        return scatter

    def change_scatter_alpha(self, dt):
        from math import cos
        self.root.alpha = abs(cos(Clock.get_boottime()))

ShaderAlphaApp().run()