from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import subprocess
import random

class MacScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        
        self.add_widget(Label(text='MAC Changer', font_size='24sp'))
        self.add_widget(Label(text='Интерфейс (wlan0):', size_hint=(1, 0.1)))
        self.iface = TextInput(text='wlan0', multiline=False)
        self.add_widget(self.iface)
        
        btn_show = Button(text='Показать текущий MAC')
        btn_show.bind(on_press=self.show_mac)
        self.add_widget(btn_show)
        
        self.mac_label = Label(text='MAC: ---', color=(0,1,0,1))
        self.add_widget(self.mac_label)
        
        btn_random = Button(text='Случайный MAC', background_color=(1,0.5,0,1))
        btn_random.bind(on_press=self.random_mac)
        self.add_widget(btn_random)
        
        self.add_widget(Label(text='Или введи свой MAC:', size_hint=(1, 0.1)))
        self.custom_mac = TextInput(hint_text='XX:XX:XX:XX:XX:XX', multiline=False)
        self.add_widget(self.custom_mac)
        
        btn_apply = Button(text='Применить MAC', background_color=(0,0.8,0,1))
        btn_apply.bind(on_press=self.apply_mac)
        self.add_widget(btn_apply)
        
        self.status = Label(text='Готов', size_hint=(1, 0.2))
        self.add_widget(self.status)
    
    def show_mac(self, instance):
        iface = self.iface.text
        try:
            result = subprocess.run(['su', '-c', f'cat /sys/class/net/{iface}/address'], 
                                    capture_output=True, text=True, timeout=2)
            mac = result.stdout.strip()
            self.mac_label.text = f'MAC: {mac}'
            self.status.text = 'MAC получен'
        except:
            self.status.text = 'Ошибка: нужен root или интерфейс не найден'
    
    def random_mac(self, instance):
        mac = [0x00, 0x16, 0x3e, random.randint(0x00,0x7f), random.randint(0x00,0xff), random.randint(0x00,0xff)]
        new_mac = ':'.join(f'{b:02x}' for b in mac)
        self.custom_mac.text = new_mac
        self.apply_mac(None)
    
    def apply_mac(self, instance):
        iface = self.iface.text
        mac = self.custom_mac.text
        self.status.text = f'Смена MAC на {mac}...'
        commands = [
            f'su -c "ip link set {iface} down"',
            f'su -c "ip link set {iface} address {mac}"',
            f'su -c "ip link set {iface} up"'
        ]
        ok = True
        for cmd in commands:
            res = subprocess.run(cmd, shell=True, capture_output=True)
            if res.returncode != 0:
                ok = False
                break
        if ok:
            self.status.text = f'✅ MAC изменён на {mac}'
            self.mac_label.text = f'MAC: {mac}'
        else:
            self.status.text = '❌ Ошибка: нет root доступа'

class MacApp(App):
    def build(self):
        return MacScreen()

if __name__ == '__main__':
    MacApp().run()
