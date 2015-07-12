#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Sun Jul 12 23:18:02 2015
##################################################

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio import vocoder
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import PyQt4.Qwt5 as Qwt
import dect2
import sys
import time

class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        try:
             self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
             pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.dect_symbol_rate = dect_symbol_rate = 1152000
        self.dect_occupied_bandwidth = dect_occupied_bandwidth = 1.2*dect_symbol_rate
        self.dect_channel_bandwidth = dect_channel_bandwidth = 1.728e6
        self.baseband_sampling_rate = baseband_sampling_rate = 100000000/32
        self.rx_gain = rx_gain = 0
        self.rx_freq = rx_freq = 1897344000
        self.resampler_filter_taps = resampler_filter_taps = firdes.low_pass_2(1, 3*baseband_sampling_rate, dect_occupied_bandwidth/2, (dect_channel_bandwidth - dect_occupied_bandwidth)/2, 30)
        self.part_id = part_id = 0

        ##################################################
        # Blocks
        ##################################################
        self._rx_gain_layout = Qt.QVBoxLayout()
        self._rx_gain_tool_bar = Qt.QToolBar(self)
        self._rx_gain_layout.addWidget(self._rx_gain_tool_bar)
        self._rx_gain_tool_bar.addWidget(Qt.QLabel("RX Gain"+": "))
        class qwt_counter_pyslot(Qwt.QwtCounter):
            def __init__(self, parent=None):
                Qwt.QwtCounter.__init__(self, parent)
            @pyqtSlot('double')
            def setValue(self, value):
                super(Qwt.QwtCounter, self).setValue(value)
        self._rx_gain_counter = qwt_counter_pyslot()
        self._rx_gain_counter.setRange(0, 30, 1)
        self._rx_gain_counter.setNumButtons(2)
        self._rx_gain_counter.setValue(self.rx_gain)
        self._rx_gain_tool_bar.addWidget(self._rx_gain_counter)
        self._rx_gain_counter.valueChanged.connect(self.set_rx_gain)
        self._rx_gain_slider = Qwt.QwtSlider(None, Qt.Qt.Horizontal, Qwt.QwtSlider.BottomScale, Qwt.QwtSlider.BgSlot)
        self._rx_gain_slider.setRange(0, 30, 1)
        self._rx_gain_slider.setValue(self.rx_gain)
        self._rx_gain_slider.setMinimumWidth(200)
        self._rx_gain_slider.valueChanged.connect(self.set_rx_gain)
        self._rx_gain_layout.addWidget(self._rx_gain_slider)
        self.top_layout.addLayout(self._rx_gain_layout)
        self._rx_freq_options = [1897344000, 1881792000, 1883520000, 1885248000, 1886876000, 1888704000, 1890432000, 1892160000, 1893888000, 1895616000,]
        self._rx_freq_labels = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self._rx_freq_tool_bar = Qt.QToolBar(self)
        self._rx_freq_tool_bar.addWidget(Qt.QLabel("Carrier Number"+": "))
        self._rx_freq_combo_box = Qt.QComboBox()
        self._rx_freq_tool_bar.addWidget(self._rx_freq_combo_box)
        for label in self._rx_freq_labels: self._rx_freq_combo_box.addItem(label)
        self._rx_freq_callback = lambda i: Qt.QMetaObject.invokeMethod(self._rx_freq_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._rx_freq_options.index(i)))
        self._rx_freq_callback(self.rx_freq)
        self._rx_freq_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_rx_freq(self._rx_freq_options[i]))
        self.top_layout.addWidget(self._rx_freq_tool_bar)
        self.vocoder_g721_decode_bs_0 = vocoder.g721_decode_bs()
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	device_addr="",
        	stream_args=uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(3125000)
        self.uhd_usrp_source_0.set_center_freq(rx_freq, 0)
        self.uhd_usrp_source_0.set_gain(rx_gain, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=6,
                decimation=1,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler = filter.rational_resampler_base_ccc(3, 2, (resampler_filter_taps))
        self._part_id_options = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self._part_id_labels = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
        self._part_id_tool_bar = Qt.QToolBar(self)
        self._part_id_tool_bar.addWidget(Qt.QLabel("Select Part"+": "))
        self._part_id_combo_box = Qt.QComboBox()
        self._part_id_tool_bar.addWidget(self._part_id_combo_box)
        for label in self._part_id_labels: self._part_id_combo_box.addItem(label)
        self._part_id_callback = lambda i: Qt.QMetaObject.invokeMethod(self._part_id_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._part_id_options.index(i)))
        self._part_id_callback(self.part_id)
        self._part_id_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_part_id(self._part_id_options[i]))
        self.top_layout.addWidget(self._part_id_tool_bar)
        self.fractional_resampler = filter.fractional_resampler_cc(0, (3.0*baseband_sampling_rate/2.0)/dect_symbol_rate/4.0)
        self.dect2_phase_diff_0 = dect2.phase_diff()
        self.dect2_packet_receiver_0 = dect2.packet_receiver()
        self.dect2_packet_decoder_0 = dect2.packet_decoder()
        self.console_0 = dect2.console()
        self.top_layout.addWidget(self.console_0)
          
        self.blocks_short_to_float_0 = blocks.short_to_float(1, 32768)
        self.audio_sink_0 = audio.sink(48000, "", True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.rational_resampler, 0), (self.fractional_resampler, 0))
        self.connect((self.fractional_resampler, 0), (self.dect2_phase_diff_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.vocoder_g721_decode_bs_0, 0), (self.blocks_short_to_float_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.rational_resampler, 0))
        self.connect((self.dect2_packet_decoder_0, 0), (self.vocoder_g721_decode_bs_0, 0))
        self.connect((self.dect2_phase_diff_0, 0), (self.dect2_packet_receiver_0, 0))
        self.connect((self.dect2_packet_receiver_0, 0), (self.dect2_packet_decoder_0, 0))
        self.connect((self.blocks_short_to_float_0, 0), (self.rational_resampler_xxx_0, 0))

        ##################################################
        # Asynch Message Connections
        ##################################################
        self.msg_connect(self.dect2_packet_decoder_0, "log_out", self.console_0, "in")
        self.msg_connect(self.dect2_packet_receiver_0, "rcvr_msg_out", self.dect2_packet_decoder_0, "rcvr_msg_in")

# QT sink close method reimplementation
    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_dect_symbol_rate(self):
        return self.dect_symbol_rate

    def set_dect_symbol_rate(self, dect_symbol_rate):
        self.dect_symbol_rate = dect_symbol_rate
        self.set_dect_occupied_bandwidth(1.2*self.dect_symbol_rate)
        self.fractional_resampler.set_resamp_ratio((3.0*self.baseband_sampling_rate/2.0)/self.dect_symbol_rate/4.0)

    def get_dect_occupied_bandwidth(self):
        return self.dect_occupied_bandwidth

    def set_dect_occupied_bandwidth(self, dect_occupied_bandwidth):
        self.dect_occupied_bandwidth = dect_occupied_bandwidth
        self.set_resampler_filter_taps(firdes.low_pass_2(1, 3*self.baseband_sampling_rate, self.dect_occupied_bandwidth/2, (self.dect_channel_bandwidth - self.dect_occupied_bandwidth)/2, 30))

    def get_dect_channel_bandwidth(self):
        return self.dect_channel_bandwidth

    def set_dect_channel_bandwidth(self, dect_channel_bandwidth):
        self.dect_channel_bandwidth = dect_channel_bandwidth
        self.set_resampler_filter_taps(firdes.low_pass_2(1, 3*self.baseband_sampling_rate, self.dect_occupied_bandwidth/2, (self.dect_channel_bandwidth - self.dect_occupied_bandwidth)/2, 30))

    def get_baseband_sampling_rate(self):
        return self.baseband_sampling_rate

    def set_baseband_sampling_rate(self, baseband_sampling_rate):
        self.baseband_sampling_rate = baseband_sampling_rate
        self.set_resampler_filter_taps(firdes.low_pass_2(1, 3*self.baseband_sampling_rate, self.dect_occupied_bandwidth/2, (self.dect_channel_bandwidth - self.dect_occupied_bandwidth)/2, 30))
        self.fractional_resampler.set_resamp_ratio((3.0*self.baseband_sampling_rate/2.0)/self.dect_symbol_rate/4.0)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        Qt.QMetaObject.invokeMethod(self._rx_gain_counter, "setValue", Qt.Q_ARG("double", self.rx_gain))
        Qt.QMetaObject.invokeMethod(self._rx_gain_slider, "setValue", Qt.Q_ARG("double", self.rx_gain))
        self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self.uhd_usrp_source_0.set_center_freq(self.rx_freq, 0)
        self._rx_freq_callback(self.rx_freq)

    def get_resampler_filter_taps(self):
        return self.resampler_filter_taps

    def set_resampler_filter_taps(self, resampler_filter_taps):
        self.resampler_filter_taps = resampler_filter_taps
        self.rational_resampler.set_taps((self.resampler_filter_taps))

    def get_part_id(self):
        return self.part_id

    def set_part_id(self, part_id):
        self.part_id = part_id
        self.dect2_packet_decoder_0.select_rx_part(self.part_id)
        self._part_id_callback(self.part_id)

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = top_block()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets

