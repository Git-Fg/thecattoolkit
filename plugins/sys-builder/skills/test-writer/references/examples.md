# Example Transformations

## Basic Example

### Documentation
```javascript
const name = 'World'
console.log('Hello, ' + name + '!') // Hello, World!
```

### Test
```javascript
it('should greet with name - Line 2', () => {
  const name = 'World'
  const result = 'Hello, ' + name + '!'
  expect(result).toBe('Hello, World!')
})
```

## Error Example

### Documentation
```javascript
function divide(a, b) {
  if (b === 0) throw new Error('Cannot divide by zero')
  return a / b
}
console.log(divide(10, 2)) // 5
```

### Test
```javascript
describe('divide', () => {
  it('should divide two numbers - Line 1', () => {
    expect(divide(10, 2)).toBe(5)
  })

  it('should throw error when dividing by zero - Line 2', () => {
    expect(() => divide(10, 0)).toThrow('Cannot divide by zero')
  })
})
```

## Async Example

### Documentation
```javascript
async function fetchData() {
  const data = await fetch('/api/data')
  return data.json()
}
console.log(await fetchData()) // { status: 'success' }
```

### Test
```javascript
it('should fetch and parse data - Line 1', async () => {
  const result = await fetchData()
  expect(result).toEqual({ status: 'success' })
})
```

## DOM Example

### Documentation
```javascript
const button = document.createElement('button')
button.textContent = 'Click me'
button.addEventListener('click', () => {
  console.log('Button clicked!')
})
document.body.appendChild(button)
```

### Test
```javascript
/**
 * @vitest-environment jsdom
 */

it('should append button to body - Line 1', () => {
  const button = document.createElement('button')
  button.textContent = 'Click me'
  document.body.appendChild(button)

  expect(document.body.contains(button)).toBe(true)
})

it('should handle click event - Line 2', () => {
  const button = document.createElement('button')
  button.textContent = 'Click me'
  const handler = vi.fn()
  button.addEventListener('click', handler)
  button.click()

  expect(handler).toHaveBeenCalledTimes(1)
})
```

## Side Effect Example

### Documentation
```javascript
const counter = { value: 0 }
function increment() {
  counter.value++
}
increment()
console.log(counter.value) // 1
```

### Test
```javascript
it('should increment counter - Line 4', () => {
  const counter = { value: 0 }
  increment(counter)
  expect(counter.value).toBe(1)
})
```
