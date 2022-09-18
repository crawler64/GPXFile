class ByteBuffer():
  def __init__(self, n, buffer):
    self.position = 0
    self.buffer = buffer

  def length(self):
    return len(self.buffer)
  
  def offset(self):
    return int(self.position / 8)
  
  def end(self):
    #print("Offset",self.offset())
    return self.offset() >= self.length()

  def readBit(self):
    n = -1
    n2 = self.offset()
    n3 = 7 - self.position % 8
    #n3 = self.position % 8
    if (n2 >= 0 and n2 < self.length()):
      n = (self.buffer[n2] & 0xFF) >> n3 & 1
      #print(self.buffer)
      self.position += 1
    return n

  def readBits(self, n):
        n2 = 0;
        #for (i = n - 1; i >= 0; --i):
        for i in reversed(range(n)):
            n2 |= self.readBit() << i
        return n2
  
  def readBitsReversed(self,n):
        n2 = 0;
        #for (int i = 0; i < n; ++i) {
        for i in range(n):
            n2 |= self.readBit() << i
        return n2

  def readBytes(self, n):
        #byte[] arrby = new byte[n];
        arrby = bytearray(n)
        #for (int i = 0; i < n; ++i) {
        for i in range(n):
            arrby[i] = self.readBits(8)
        return arrby