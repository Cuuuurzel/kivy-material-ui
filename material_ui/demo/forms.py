import pdb
import sys
sys.path.append( '..' )

from kivy.app import App
from kivy.atlas import Atlas
from kivy.cache import Cache
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from material_ui.navigation.form import Form
from material_ui.navigation.error import ErrorForm
from material_ui.navigation.nonetwork import NoNetworkForm

from material_ui.flatui.flatui import FloatingAction
from material_ui.flatui.popups import AlertPopup, FlatPopup, PopupComboBox, PopupListView
from material_ui.flatui.scroll import RefreshableScrollView

#KV Lang files
from pkg_resources import resource_filename
path = resource_filename( __name__, 'forms.kv' )
icon_done = resource_filename( __name__, '../images/done-32.png' )
Builder.load_file( path )


class Screen1( Form ) :
    '''
    Showcase for buttons and popups.
    '''

    def __init__( self, **kargs ) :
        super( Screen1, self ).__init__( **kargs )

    def show_flat_popup( self ) :
        txt = 'FlatPopup has attributed title'
        lbl = Label( text=txt )
        popup = FlatPopup( 
            title='Flat popup',
            size_hint=(.8,.8), 
            content=lbl 
        )
        popup.open()

    def show_alert_popup( self ) :
        txt = 'AlertPopup comes with two buttons.\nYou can set callbacks on them.'
        popup = AlertPopup( 
            title='Alert popup', 
            ok_button_text='YES', cancel_button_text='NO',
            text=txt, size_hint=(.8,.6)
        )
        popup.open()

    def show_okbutton_popup( self ) :
        txt = "Use AlertPopup with a single 'OK' button."
        popup = AlertPopup( 
            title='Ok button popup', 
            text=txt, 
            size_hint=(.8,.6)
        )        
        popup.open()

    def show_popup_list_view( self ) :
        data = 'Mario Maria Luigi Gianni Federico Alessandro Massimo Mattia'.split(' ')
        popup = PopupListView( 
            data, 
            size_hint=[.5,.8],
            title='Stateless value-picker', 
        )
        popup.open()

    def next_page( self ) :
        Screen2( 
            shared_navigation_controller=self.shared_navigation_controller 
        ).push()
        

class Screen2( Form ) :
    '''
    Showcase for RefreshableScrollView and ErrorForm.
    '''

    def __init__( self, **kargs ) :
        super( Screen2, self ).__init__( **kargs )

        """
        ScrollView with a refresh controll...
        """
        self.myscroll = RefreshableScrollView( 
            on_start_reload=self.on_start_reload, 
            root_layout=self.shared_navigation_controller.floating_panel
        )
        self.add_widget( self.myscroll )
            
        """
        Loading fake elements...
        """
        temp = GridLayout( size_hint=(1,None), cols=1 )
        for n in ['Pull down to reload','A fake error will be raised']+list(range(0,20)) :
            l = Label( text='Element no '+str(n), height=dp(50), size_hint=(1,None), color=[0,0,0,.8] )
            temp.add_widget( l )
            temp.height += dp(50)

        self.myscroll.add_widget( temp )

    """
    Called whenever the user asks for a refresh of the scrollview.
    """
    def on_start_reload( self, *args ) :
        Clock.schedule_once( self.raise_fake_error, 5 )

    """
    Will show an error form.
    """
    def raise_fake_error( self, *args ) :
        self.myscroll.reload_done()
        try :        
           raise IOError( "Fake exeption to show pop\\push animations." )
        except IOError as e :
            self.shared_navigation_controller.push( 
                NoNetworkForm(
                    shared_navigation_controller=self.shared_navigation_controller, 
                    strace=str(e) 
                ), 
                title='Network Error'
            )
        except Exception as e :
            self.shared_navigation_controller.push( 
                ErrorForm( 
                    shared_navigation_controller=self.shared_navigation_controller,
                    strace=str(e) 
                ), 
                title='Generic Error' 
            )
        return True
    
    def on_push( self, controller ) :

        self.fbutton = FloatingAction(
            icon=icon_done,
            diameter=dp(56),
            size_hint=(None,None),
            background_color=( 1, .1, .1, 1 ),
            background_color_down=( .9, .1, .1, 1 ),
            color=[1,1,1,1]
        )
        self.fbutton.bind( on_press=self.fbutton_press )
        self.fbutton.add_to_bottom_right( 
            self.shared_navigation_controller.floating_panel
        )

    def on_pop( self, controller ) :
        self.fbutton.remove_from_parent()

    def fbutton_press( self, instance ) :
        Screen3( 
            shared_navigation_controller=self.shared_navigation_controller 
        ).push()


class Screen3( Form ) :
    
    pass




