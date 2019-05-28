package main

import "fmt"

func ReverseArray(data []int, start int, end int) {
    i := start
    j := end
    for i < j{
      data[i], data[j] = data[j], data[i]
      i++
      j++
    }
}

func RotateArray(data []int, k int) {
  n := len(data)
  ReverseArray(data, 0, k-1)
  ReverseArray(data, k, n-1)
  ReverseArray(data, 0, n-1)
}

func main() {
  datas := []int{1,2,3,4,5,6,7,8}
  val := 3
  fmt.Println("call rotate array from reverse array")
  RotateArray(datas,val)
  fmt.Println(datas)
}
