package main
import (
  "fmt"
)

func BinarySearch(data []int, value int) bool {
  size := len(data)
  var mid int
  low := 0
  high := size - 1
  for low <= high {
    mid = low + (high-low)/2
    if data[mid] == value {
      return true
    } else {
      if data[mid] < value {
        low = mid + 1
      } else {
        high = mid - 1
      }
    }
  }
  return false
}

func main () {
  datas := []int{1,4,8,10,11,12,24,25}
  val := 9
  fmt.Println("call function binary search")
  fmt.Println(BinarySearch(datas,val))
}
