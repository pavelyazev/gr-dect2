#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Top Block
# GNU Radio version: v3.9.2.0-95-g02c0d949

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio import vocoder
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import dect2



from gnuradio import qtgui

class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        qtgui.util.check_set_qss()
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

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

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
        self.resample_ratio = resample_ratio = int((3.0*baseband_sampling_rate/2.0)/dect_symbol_rate/4.0)
        self.part_id = part_id = 0

        ##################################################
        # Blocks
        ##################################################
        self._rx_gain_range = Range(0, 30, 1, 0, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, 'RX Gain', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rx_gain_win)
        # Create the options list
        self._rx_freq_options = [1897344000, 1895616000, 1893888000, 1892160000, 1890432000, 1888704000, 1886876000, 1885248000, 1883520000, 1881792000, 1899072000, 1900800000, 1902528000, 1904256000, 1905984000, 1907712000, 1909440, 1911168000, 1912896000, 1914624000, 1916352000, 1918080000, 1919808000, 1921536000, 1923264000, 1924992000, 1926720000, 1928448000, 1930176000, 1931904000, 1933632000, 1935360000, 1937088000]
        # Create the labels list
        self._rx_freq_labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32']
        # Create the combo box
        self._rx_freq_tool_bar = Qt.QToolBar(self)
        self._rx_freq_tool_bar.addWidget(Qt.QLabel('Carrier Number' + ": "))
        self._rx_freq_combo_box = Qt.QComboBox()
        self._rx_freq_tool_bar.addWidget(self._rx_freq_combo_box)
        for _label in self._rx_freq_labels: self._rx_freq_combo_box.addItem(_label)
        self._rx_freq_callback = lambda i: Qt.QMetaObject.invokeMethod(self._rx_freq_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._rx_freq_options.index(i)))
        self._rx_freq_callback(self.rx_freq)
        self._rx_freq_combo_box.currentIndexChanged.connect(
            lambda i: self.set_rx_freq(self._rx_freq_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._rx_freq_tool_bar)
        self.vocoder_g721_decode_bs_0 = vocoder.g721_decode_bs()
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(('', "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(3125000)
        # No synchronization enforced.

        self.uhd_usrp_source_0.set_center_freq(rx_freq, 0)
        self.uhd_usrp_source_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_source_0.set_gain(rx_gain, 0)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=3,
                decimation=2,
                taps=resampler_filter_taps,
                fractional_bw=0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=6,
                decimation=1,
                taps=[],
                fractional_bw=0)
        # Create the options list
        self._part_id_options = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
        # Create the labels list
        self._part_id_labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32']
        # Create the combo box
        self._part_id_tool_bar = Qt.QToolBar(self)
        self._part_id_tool_bar.addWidget(Qt.QLabel('Select Part' + ": "))
        self._part_id_combo_box = Qt.QComboBox()
        self._part_id_tool_bar.addWidget(self._part_id_combo_box)
        for _label in self._part_id_labels: self._part_id_combo_box.addItem(_label)
        self._part_id_callback = lambda i: Qt.QMetaObject.invokeMethod(self._part_id_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._part_id_options.index(i)))
        self._part_id_callback(self.part_id)
        self._part_id_combo_box.currentIndexChanged.connect(
            lambda i: self.set_part_id(self._part_id_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._part_id_tool_bar)
        self.mmse_resampler_xx_0 = filter.mmse_resampler_cc(0, resample_ratio)
        self.dect2_phase_diff_0 = dect2.phase_diff()
        self.dect2_packet_receiver_0 = dect2.packet_receiver()
        self.dect2_packet_decoder_0 = dect2.packet_decoder()
        self.console_0 = dect2.console()
        self.top_layout.addWidget(self.console_0)
        self.blocks_short_to_float_0 = blocks.short_to_float(1, 32768)
        self.audio_sink_0 = audio.sink(48000, 'plughw:0,0', True)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.dect2_packet_decoder_0, 'log_out'), (self.console_0, 'in'))
        self.msg_connect((self.dect2_packet_receiver_0, 'rcvr_msg_out'), (self.dect2_packet_decoder_0, 'rcvr_msg_in'))
        self.connect((self.blocks_short_to_float_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.dect2_packet_decoder_0, 0), (self.vocoder_g721_decode_bs_0, 0))
        self.connect((self.dect2_packet_receiver_0, 0), (self.dect2_packet_decoder_0, 0))
        self.connect((self.dect2_phase_diff_0, 0), (self.dect2_packet_receiver_0, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.dect2_phase_diff_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.mmse_resampler_xx_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.vocoder_g721_decode_bs_0, 0), (self.blocks_short_to_float_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_dect_symbol_rate(self):
        return self.dect_symbol_rate

    def set_dect_symbol_rate(self, dect_symbol_rate):
        self.dect_symbol_rate = dect_symbol_rate
        self.set_dect_occupied_bandwidth(1.2*self.dect_symbol_rate)
        self.set_resample_ratio(int((3.0*self.baseband_sampling_rate/2.0)/self.dect_symbol_rate/4.0))

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
        self.set_resample_ratio(int((3.0*self.baseband_sampling_rate/2.0)/self.dect_symbol_rate/4.0))
        self.set_resampler_filter_taps(firdes.low_pass_2(1, 3*self.baseband_sampling_rate, self.dect_occupied_bandwidth/2, (self.dect_channel_bandwidth - self.dect_occupied_bandwidth)/2, 30))

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self._rx_freq_callback(self.rx_freq)
        self.uhd_usrp_source_0.set_center_freq(self.rx_freq, 0)

    def get_resampler_filter_taps(self):
        return self.resampler_filter_taps

    def set_resampler_filter_taps(self, resampler_filter_taps):
        self.resampler_filter_taps = resampler_filter_taps
        self.rational_resampler_xxx_1.set_taps(self.resampler_filter_taps)

    def get_resample_ratio(self):
        return self.resample_ratio

    def set_resample_ratio(self, resample_ratio):
        self.resample_ratio = resample_ratio
        self.mmse_resampler_xx_0.set_resamp_ratio(self.resample_ratio)

    def get_part_id(self):
        return self.part_id

    def set_part_id(self, part_id):
        self.part_id = part_id
        self._part_id_callback(self.part_id)
        self.dect2_packet_decoder_0.select_rx_part(self.part_id)




def main(top_block_cls=top_block, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
