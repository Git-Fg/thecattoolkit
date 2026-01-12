# Agent Coordination

## What is Agent Coordination?

Agent coordination is the **communication and synchronization** between multiple agents working on a shared task. It ensures agents work together effectively, share information appropriately, and produce coherent results.

## Types of Coordination

### 1. Direct Coordination

Agents communicate **directly** with each other.

```javascript
// Agent A requests data from Agent B
const result = await agentB.execute({
  type: 'data_request',
  query: 'customer_churn_data'
})

// Agent A uses result
return this.process(result.data)
```

**Pros:**
- Simple to implement
- Low latency
- Direct communication

**Cons:**
- Tight coupling
- Hard to scale
- Complex dependency management

### 2. Mediated Coordination

Agents communicate through a **coordinator**.

```javascript
// Agent A requests data via coordinator
coordinator.request({
  from: agentA,
  to: agentB,
  type: 'data_request',
  query: 'customer_churn_data'
})

// Coordinator routes to Agent B
const result = agentB.execute(request)

// Coordinator routes back to Agent A
return coordinator.respond(result)
```

**Pros:**
- Loose coupling
- Better monitoring
- Easier to scale

**Cons:**
- Additional overhead
- Coordinator becomes bottleneck
- More complex

### 3. Shared Memory Coordination

Agents communicate through **shared data structures**.

```javascript
// Agent A writes to shared memory
sharedMemory.set('data_for_agent_b', data)

// Agent B reads from shared memory
const data = sharedMemory.get('data_for_agent_b')

// Agent B writes result
sharedMemory.set('result_for_agent_a', result)

// Agent A reads result
const result = sharedMemory.get('result_for_agent_a')
```

**Pros:**
- Decoupled timing
- Easy to add agents
- Shared state

**Cons:**
- Synchronization issues
- Potential conflicts
- Memory management

### 4. File-Based Coordination

Agents communicate through **files**.

```javascript
// Agent A writes task file
await fs.writeFile('task_for_b.json', JSON.stringify(task))

// Agent B reads task file
const task = JSON.parse(await fs.readFile('task_for_b.json'))

// Agent B writes result file
await fs.writeFile('result_for_a.json', JSON.stringify(result))

// Agent A reads result file
const result = JSON.parse(await fs.readFile('result_for_a.json'))
```

**Pros:**
- Decoupled execution
- Persistent
- Easy debugging
- Language agnostic

**Cons:**
- I/O overhead
- File system dependency
- Cleanup needed

## Coordination Patterns

### Pattern 1: Request-Response

```javascript
class RequestResponseCoordinator {
  async request(fromAgent, toAgent, request) {
    const requestId = this.generateId()

    // Store pending request
    this.pending[requestId] = {
      from: fromAgent,
      request: request,
      timestamp: Date.now()
    }

    // Send to target agent
    const response = await toAgent.execute(request)

    // Return to requesting agent
    return response
  }
}
```

### Pattern 2: Publish-Subscribe

```javascript
class PubSubCoordinator {
  constructor() {
    this.subscribers = new Map()
    this.topics = new Map()
  }

  subscribe(agent, topic) {
    if (!this.subscribers.has(topic)) {
      this.subscribers.set(topic, new Set())
    }
    this.subscribers.get(topic).add(agent)
  }

  publish(topic, message) {
    const agents = this.subscribers.get(topic) || new Set()

    for (const agent of agents) {
      agent.notify(topic, message)
    }
  }
}
```

### Pattern 3: Blackboard

```javascript
class BlackboardCoordinator {
  constructor() {
    this.blackboard = new SharedMemory()
    this.agents = new Set()
  }

  register(agent) {
    this.agents.add(agent)
    agent.setBlackboard(this.blackboard)
  }

  // Agents write to blackboard
  write(agentId, key, value) {
    this.blackboard.set(key, {
      value: value,
      writer: agentId,
      timestamp: Date.now()
    })
  }

  // Agents read from blackboard
  read(key) {
    return this.blackboard.get(key)
  }

  // Notify other agents of changes
  notify(agentId, key, value) {
    for (const agent of this.agents) {
      if (agent.id !== agentId) {
        agent.onBlackboardChange(key, value)
      }
    }
  }
}
```

### Pattern 4: Token Passing

```javascript
class TokenPassingCoordinator {
  constructor() {
    this.token = {
      holder: null,
      data: null,
      queue: []
    }
  }

  async request(agentId, data) {
    if (this.token.holder === null) {
      // Grant token immediately
      this.token.holder = agentId
      this.token.data = data
      return data
    } else {
      // Add to queue
      this.token.queue.push({ agentId, data })
      return this.waitForToken(agentId)
    }
  }

  async passToken(agentId, result) {
    if (this.token.holder === agentId) {
      this.token.holder = null

      if (this.token.queue.length > 0) {
        const next = this.token.queue.shift()
        this.token.holder = next.agentId
        this.token.data = next.data

        // Notify next agent
        this.notifyAgent(next.agentId)
      }
    }
  }
}
```

## Synchronization Mechanisms

### 1. Locks and Mutexes

```javascript
class Mutex {
  constructor() {
    this.locked = false
    this.queue = []
  }

  async acquire() {
    if (!this.locked) {
      this.locked = true
      return
    }

    return new Promise(resolve => {
      this.queue.push(resolve)
    })
  }

  release() {
    if (this.queue.length > 0) {
      const resolve = this.queue.shift()
      this.locked = true
      resolve()
    } else {
      this.locked = false
    }
  }

  async withLock(fn) {
    await this.acquire()
    try {
      return await fn()
    } finally {
      this.release()
    }
  }
}
```

### 2. Barriers

```javascript
class Barrier {
  constructor(count) {
    this.count = count
    this.reached = 0
    this.waiters = []
  }

  async wait() {
    this.reached++

    if (this.reached < this.count) {
      // Wait for others
      return new Promise(resolve => {
        this.waiters.push(resolve)
      })
    } else {
      // All reached, release all
      this.reached = 0
      const waiters = [...this.waiters]
      this.waiters = []

      for (const resolve of waiters) {
        resolve()
      }
    }
  }
}
```

### 3. Condition Variables

```javascript
class Condition {
  constructor() {
    this.waiters = []
    this.predicate = () => false
  }

  setPredicate(predicate) {
    this.predicate = predicate
    this.check()
  }

  async wait() {
    if (this.predicate()) {
      return
    }

    return new Promise(resolve => {
      this.waiters.push(resolve)
    })
  }

  notify() {
    this.check()
  }

  notifyAll() {
    while (this.waiters.length > 0) {
      this.check()
    }
  }

  check() {
    if (this.predicate() && this.waiters.length > 0) {
      const resolve = this.waiters.shift()
      resolve()
    }
  }
}
```

## Conflict Resolution

### Strategy 1: Priority-Based

```javascript
class PriorityCoordinator {
  async resolve(requests) {
    // Sort by priority
    requests.sort((a, b) => b.priority - a.priority)

    // Grant to highest priority
    return requests[0]
  }
}
```

### Strategy 2: First-Come-First-Served

```javascript
class FCFSCoordinator {
  constructor() {
    this.queue = []
  }

  async enqueue(request) {
    this.queue.push({
      request: request,
      timestamp: Date.now()
    })
  }

  async dequeue() {
    if (this.queue.length === 0) {
      return null
    }

    return this.queue.shift().request
  }
}
```

### Strategy 3: Voting

```javascript
class VotingCoordinator {
  async vote(requests) {
    const voteCounts = new Map()

    // Count votes
    for (const request of requests) {
      const key = this.getRequestKey(request)
      voteCounts.set(key, (voteCounts.get(key) || 0) + 1)
    }

    // Find majority
    const sorted = [...voteCounts.entries()]
      .sort((a, b) => b[1] - a[1])

    return sorted[0][0]
  }

  getRequestKey(request) {
    // Create canonical representation
    return JSON.stringify({
      type: request.type,
      data: request.data
    })
  }
}
```

### Strategy 4: Arbitration

```javascript
class ArbitrationCoordinator {
  constructor(arbitrator) {
    this.arbitrator = arbitrator
  }

  async resolve(requests) {
    return this.arbitrator.decide(requests)
  }
}

// Example arbitrator
class CustomArbitrator {
  decide(requests) {
    // Custom logic
    if (requests.some(r => r.type === 'emergency')) {
      return requests.find(r => r.type === 'emergency')
    }

    return requests[0] // Default to first
  }
}
```

## Error Handling

### Retry Logic

```javascript
class RetryCoordinator {
  async executeWithRetry(agent, task, maxRetries = 3) {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        return await agent.execute(task)
      } catch (error) {
        if (attempt === maxRetries) {
          throw error
        }

        // Exponential backoff
        await this.delay(Math.pow(2, attempt) * 1000)

        // Retry with same or modified task
        task = this.adjustTask(task, error, attempt)
      }
    }
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
  }

  adjustTask(task, error, attempt) {
    // Simplify task on retry
    return {
      ...task,
      constraints: {
        ...task.constraints,
        maxRetries: 0 // Prevent infinite recursion
      }
    }
  }
}
```

### Circuit Breaker

```javascript
class CircuitBreaker {
  constructor(threshold = 5, timeout = 60000) {
    this.threshold = threshold
    this.timeout = timeout
    this.failureCount = 0
    this.lastFailureTime = null
    this.state = 'CLOSED' // CLOSED, OPEN, HALF_OPEN
  }

  async execute(operation) {
    if (this.state === 'OPEN') {
      if (this.shouldAttemptReset()) {
        this.state = 'HALF_OPEN'
      } else {
        throw new Error('Circuit breaker is OPEN')
      }
    }

    try {
      const result = await operation()
      this.onSuccess()
      return result
    } catch (error) {
      this.onFailure()
      throw error
    }
  }

  onSuccess() {
    this.failureCount = 0
    this.state = 'CLOSED'
  }

  onFailure() {
    this.failureCount++
    this.lastFailureTime = Date.now()

    if (this.failureCount >= this.threshold) {
      this.state = 'OPEN'
    }
  }

  shouldAttemptReset() {
    return Date.now() - this.lastFailureTime > this.timeout
  }
}
```

## Deadlock Prevention

### Strategy 1: Resource Ordering

```javascript
// Always acquire locks in the same order
class OrderedLock {
  constructor(resourceId) {
    this.resourceId = resourceId
  }

  async acquire(locks) {
    // Sort locks by resource ID
    const sorted = locks.sort((a, b) => a.resourceId.localeCompare(b.resourceId))

    for (const lock of sorted) {
      await lock.acquire()
    }
  }
}
```

### Strategy 2: Timeout

```javascript
class TimeoutCoordinator {
  async requestWithTimeout(request, timeout = 5000) {
    const result = await Promise.race([
      this.executeRequest(request),
      this.timeout(timeout)
    ])

    return result
  }

  timeout(ms) {
    return new Promise((_, reject) => {
      setTimeout(() => reject(new Error('Timeout')), ms)
    })
  }
}
```

### Strategy 3: Deadlock Detection

```javascript
class DeadlockDetector {
  constructor() {
    this.waitForGraph = new Map()
  }

  detectDeadlock() {
    const graph = this.buildWaitForGraph()

    // Check for cycles
    return this.hasCycle(graph)
  }

  buildWaitForGraph() {
    const graph = new Map()

    for (const [agent, waitingFor] of this.waitForGraph.entries()) {
      if (!graph.has(agent)) {
        graph.set(agent, new Set())
      }

      graph.get(agent).add(waitingFor)
    }

    return graph
  }

  hasCycle(graph) {
    const visited = new Set()
    const recursionStack = new Set()

    for (const node of graph.keys()) {
      if (this.hasCycleDFS(node, graph, visited, recursionStack)) {
        return true
      }
    }

    return false
  }

  hasCycleDFS(node, graph, visited, recursionStack) {
    visited.add(node)
    recursionStack.add(node)

    for (const neighbor of graph.get(node) || []) {
      if (!visited.has(neighbor)) {
        if (this.hasCycleDFS(neighbor, graph, visited, recursionStack)) {
          return true
        }
      } else if (recursionStack.has(neighbor)) {
        return true
      }
    }

    recursionStack.delete(node)
    return false
  }
}
```

## Load Balancing

### Round Robin

```javascript
class RoundRobinBalancer {
  constructor(agents) {
    this.agents = agents
    this.index = 0
  }

  getNextAgent() {
    const agent = this.agents[this.index]
    this.index = (this.index + 1) % this.agents.length
    return agent
  }
}
```

### Least Loaded

```javascript
class LeastLoadedBalancer {
  constructor(agents) {
    this.agents = agents.map(agent => ({
      agent: agent,
      load: 0
    }))
  }

  getNextAgent() {
    // Return agent with lowest load
    const sorted = this.agents.sort((a, b) => a.load - b.load)
    return sorted[0].agent
  }

  updateLoad(agentId, delta) {
    const entry = this.agents.find(a => a.agent.id === agentId)
    if (entry) {
      entry.load += delta
    }
  }
}
```

## Monitoring and Metrics

### Key Metrics

```javascript
class CoordinationMetrics {
  track(request) {
    return {
      requestId: request.id,
      agentId: request.agentId,
      startTime: Date.now(),
      coordinationTime: null,
      result: null,
      errors: []
    }
  }

  recordSuccess(metrics, result) {
    metrics.coordinationTime = Date.now() - metrics.startTime
    metrics.result = 'success'
    return metrics
  }

  recordError(metrics, error) {
    metrics.errors.push(error)
    metrics.result = 'error'
    return metrics
  }

  aggregate(allMetrics) {
    return {
      totalRequests: allMetrics.length,
      successRate: this.calculateSuccessRate(allMetrics),
      averageLatency: this.calculateAverageLatency(allMetrics),
      errorRate: this.calculateErrorRate(allMetrics),
      throughput: this.calculateThroughput(allMetrics)
    }
  }
}
```

## Best Practices

### Do's ✅

✅ **Define clear interfaces**
- Specify message formats
- Document protocols
- Version interfaces

✅ **Use structured communication**
- JSON, XML, Protocol Buffers
- Consistent schemas
- Type safety

✅ **Handle errors gracefully**
- Implement retries
- Use circuit breakers
- Log failures

✅ **Monitor coordination**
- Track metrics
- Detect bottlenecks
- Alert on issues

✅ **Design for failure**
- Assume agents will fail
- Implement timeouts
- Have fallback plans

### Don'ts ❌

❌ **Don't tight couple agents**
- Use mediators
- Avoid direct dependencies
- Keep interfaces abstract

❌ **Don't block on slow agents**
- Use async/await
- Implement timeouts
- Consider cancellation

❌ **Don't ignore scalability**
- Plan for many agents
- Avoid single coordinator bottlenecks
- Use load balancing

❌ **Don't skip testing**
- Test coordination logic
- Simulate failures
- Test under load

❌ **Don't hardcode delays**
- Use adaptive timeouts
- Monitor performance
- Adjust based on metrics

## Conclusion

Effective coordination is **critical** for multi-agent systems:

1. **Choose the right pattern** - Match coordination to use case
2. **Handle failures** - Implement retries, timeouts, circuit breakers
3. **Prevent deadlocks** - Use ordering, timeouts, detection
4. **Balance load** - Distribute work evenly
5. **Monitor continuously** - Track metrics, detect issues

Remember:
- Simple coordination first
- Add complexity incrementally
- Test thoroughly
- Monitor in production

The goal: Agents work together seamlessly to solve complex tasks.
