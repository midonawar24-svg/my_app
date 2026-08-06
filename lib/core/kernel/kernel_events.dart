enum KernelEventType { initialized, conversationCreated, messageReceived, memoryStored, shutdown }
class KernelEvent { final KernelEventType type; final Map<String, dynamic> payload; final DateTime timestamp; KernelEvent({required this.type, this.payload = const {}, DateTime? timestamp}) : timestamp = timestamp ?? DateTime.now(); }
