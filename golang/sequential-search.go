package main
import "fmt"

func seqsearch(data []int, value int) bool {
  size := len(data)
  for i := 0; i < size; i++ {
    if value == data[i] {
      return true
    }
  }
  return false
}

func main() {
  datas := []int{1,3,6,2,10,4,3}
  val := 5
  fmt.Println("call function sequent search")
  fmt.Println(seqsearch(datas,val))
}
