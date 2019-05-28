package main
import "fmt"

func main() {
  s := []int {2,3,1,5,4}
  fmt.Println("test")
  fmt.Println(s)
  fmt.Println(SumArray(s))
}

func SumArray(data []int) int {
  size := len(data)
  total := 0
  for index := 0; index < size; index++ {
    total = total + data[index]
  }
  return total
}
