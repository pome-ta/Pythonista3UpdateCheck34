import ctypes
from objc_util import ObjCClass, ObjCBlock

import pdbg

CHANNEL = 1

OSStatus = ctypes.c_int32

AVAudioEngine = ObjCClass('AVAudioEngine')
AVAudioSourceNode = ObjCClass('AVAudioSourceNode')
AVAudioFormat = ObjCClass('AVAudioFormat')


class AudioTimeStampFlags(ctypes.c_uint32):
  kAudioTimeStampNothingValid = (0)
  kAudioTimeStampSampleTimeValid = (1 << 0)
  kAudioTimeStampHostTimeValid = (1 << 1)
  kAudioTimeStampRateScalarValid = (1 << 2)
  kAudioTimeStampWordClockTimeValid = (1 << 3)
  kAudioTimeStampSMPTETimeValid = (1 << 4)
  kAudioTimeStampSampleHostTimeValid = (kAudioTimeStampSampleTimeValid
                                        | kAudioTimeStampHostTimeValid)


class SMPTETimeType(ctypes.c_uint32):
  kSMPTETimeType24 = 0
  kSMPTETimeType25 = 1
  kSMPTETimeType30Drop = 2
  kSMPTETimeType30 = 3
  kSMPTETimeType2997 = 4
  kSMPTETimeType2997Drop = 5
  kSMPTETimeType60 = 6
  kSMPTETimeType5994 = 7
  kSMPTETimeType60Drop = 8
  kSMPTETimeType5994Drop = 9
  kSMPTETimeType50 = 10
  kSMPTETimeType2398 = 11


class SMPTETimeFlags(ctypes.c_uint32):
  kSMPTETimeUnknown = 0
  kSMPTETimeValid = (1 << 0)
  kSMPTETimeRunning = (1 << 1)


class SMPTETime(ctypes.Structure):
  _fields_ = [
    ('mSubframes', ctypes.c_int16),
    ('mSubframeDivisor', ctypes.c_int16),
    ('mCounter', ctypes.c_uint32),
    ('mType', SMPTETimeType),
    ('mFlags', SMPTETimeFlags),
    ('mHours', ctypes.c_int16),
    ('mMinutes', ctypes.c_int16),
    ('mSeconds', ctypes.c_int16),
    ('mFrames', ctypes.c_int16),
  ]


class AudioTimeStamp(ctypes.Structure):
  _fields_ = [
    ('mFlags', AudioTimeStampFlags),
    ('mHostTime', ctypes.c_int64),
    ('mRateScalar', ctypes.c_double),
    ('mReserved', ctypes.c_uint32),
    ('mSMPTETime', SMPTETime),
    ('mSampleTime', ctypes.c_double),
    ('mWordClockTime', ctypes.c_uint64),
  ]


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


def source_node_render(_cmd, _isSilence_ptr, _timestamp_ptr, frameCount,
                       outputData_ptr) -> OSStatus:
  # todo: ここに処理を書く
  print('test')
  return 1


render_block = ObjCBlock(
  source_node_render,
  restype=OSStatus,
  argtypes=[
    ctypes.c_void_p,  # _cmd
    ctypes.POINTER(ctypes.c_bool),  # isSilence
    ctypes.POINTER(AudioTimeStamp),  # timestamp
    ctypes.c_uint32,  # frameCount
    ctypes.POINTER(AudioBufferList),  # outputData
  ])




class Synth:

  def __init__(self):
    self.audioEngine: AVAudioEngine
    self.sampleRate: float = 44100.0  # set_up メソッド: outputNode より確定
    self.deltaTime: float = 0.0  # 1/sampleRate 時間間隔

    self.set_up()

  def set_up(self):
    audioEngine = AVAudioEngine.new()
    sourceNode = AVAudioSourceNode.alloc()
    mainMixer = audioEngine.mainMixerNode()
    outputNode = audioEngine.outputNode()
    format = outputNode.inputFormatForBus_(0)

    self.sampleRate = format.sampleRate()
    self.deltaTime = 1 / self.sampleRate

    inputFormat = AVAudioFormat.alloc(
    ).initWithCommonFormat_sampleRate_channels_interleaved_(
      format.commonFormat(), self.sampleRate, CHANNEL, format.isInterleaved())

    #sourceNode.initWithFormat_renderBlock_(inputFormat, self.render_block)
    sourceNode.initWithFormat_renderBlock_(inputFormat, render_block)
    audioEngine.attachNode_(sourceNode)
    sourceNode.volume = 0.2

    audioEngine.connect_to_format_(sourceNode, mainMixer, inputFormat)
    audioEngine.connect_to_format_(mainMixer, outputNode, inputFormat)

    audioEngine.prepare()
    self.audioEngine = audioEngine

  def start(self):
    print('a')
    b = self.audioEngine.startAndReturnError_(None)
    print(b)

  def stop(self):
    self.audioEngine.stop()


if __name__ == '__main__':
  synth = Synth()
  synth.start()

