import ctypes
from objc_util import ObjCClass, ObjCBlock, on_main_thread, ObjCInstance, ns
import ui

import pdbg

CHANNEL = 1

OSStatus = ctypes.c_int32

AVAudioEngine = ObjCClass('AVAudioEngine')
AVAudioSourceNode = ObjCClass('AVAudioSourceNode')
AVAudioFormat = ObjCClass('AVAudioFormat')


class AudioBuffer(ctypes.Structure):
  _fields_ = [
    ('mNumberChannels', ctypes.c_uint32),
    ('mDataByteSize', ctypes.c_uint32),
    ('mData', ctypes.c_void_p),
  ]


class AudioBufferList(ctypes.Structure):
  _fields_ = [
    ('mNumberBuffers', ctypes.c_uint32),
    ('mBuffers', AudioBuffer * CHANNEL),
  ]


class Synth:

  def __init__(self):
    self.audioEngine: AVAudioEngine
    self.sampleRate: float = 44100.0  # set_up メソッド: outputNode より確定
    self.deltaTime: float = 0.0  # 1/sampleRate 時間間隔

    self.render_block = ObjCBlock(
      self.source_node_render,
      #restype=OSStatus,
      ctypes.c_void_p,
      argtypes=[
        ctypes.c_void_p,  # _cmd
        ctypes.c_void_p,  # isSilence
        ctypes.c_void_p,  # timestamp
        ctypes.c_void_p,  # frameCount
        ctypes.POINTER(AudioBufferList),  # outputData
        #AudioBufferList,  # outputData
      ])

    self.set_up()

  @on_main_thread
  def set_up(self):
    audioEngine = AVAudioEngine.new()  #.autorelease()
    sourceNode = AVAudioSourceNode.alloc()
    #sourceNode = AVAudioSourceNode.new()
    mainMixer = audioEngine.mainMixerNode()
    outputNode = audioEngine.outputNode()
    format = outputNode.inputFormatForBus_(0)

    self.sampleRate = format.sampleRate()
    self.deltaTime = 1 / self.sampleRate

    inputFormat = AVAudioFormat.alloc(
    ).initWithCommonFormat_sampleRate_channels_interleaved_(
      format.commonFormat(), self.sampleRate, CHANNEL,
      format.isInterleaved())  #.autorelease()

    sourceNode.initWithFormat_renderBlock_(inputFormat,
                                           self.render_block).autorelease()

    audioEngine.attachNode_(sourceNode)
    sourceNode.volume = 0.2

    audioEngine.connect_to_format_(sourceNode, mainMixer, inputFormat)
    audioEngine.connect_to_format_(mainMixer, outputNode, inputFormat)

    audioEngine.prepare()
    self.audioEngine = audioEngine

  #@on_main_thread
  def source_node_render(self, _cmd, _isSilence_ptr, _timestamp_ptr,
                         frameCount, outputData_ptr) -> OSStatus:
    # todo: ここに処理を書く
    print('test')
    return 0

  #@on_main_thread
  def start(self):
    print('start')
    self.audioEngine.startAndReturnError_(None)  #.autorelease()
    print('startAndReturnError')

  def stop(self):
    self.audioEngine.stop()


if __name__ == '__main__':
  synth = Synth()
  #synth.start()

