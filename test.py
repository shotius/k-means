import random 
import math


NUM_CLUSTERS = 2 # კლასტერების რაოდენობა
TOTAL_DATA = 7 # წერტილთა საერთო რაოდენობა
LOWEST_SAMPLE_POINT = 0 # მინიმალური წერტილის ნომერი წერტილთა სიასში
HIGHEST_SAMPLE_POINT = 3 # მაქსიმალური წერტილის ნომრეი წერტილთა სიაში
BIG_NUMBER = math.pow(10, 10)

# წერტილთა სია
SAMPLES = [[1.0, 1.0], [1.5, 2.0], [3.0, 4.0], [5.0, 7.0], [3.5, 5.0], [4.5, 5.0], [3.5, 4.5]]

data = []
centroids = []

# წერტილთა კლასი
class DataPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def set_x(self, x):
        self.x = x
    
    def get_x(self):
        return self.x
    
    def set_y(self, y):
        self.y = y
    
    def get_y(self):
        return self.y
    
    def set_cluster(self, clusterNumber):
        self.clusterNumber = clusterNumber
    
    def get_cluster(self):
        return self.clusterNumber

# ცენტროიდთა კლასი
class Centroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def set_x(self, x):
        self.x = x
    
    def get_x(self):
        return self.x
    
    def set_y(self, y):
        self.y = y
    
    def get_y(self):
        return self.y

# ცენტროიდების ობიექტების შექმნა და მათი დამატება ცენტროიდების მასივში
def initialize_centroids():
    # ცენტროიდების კოორდინატებად ამოვირჩიოთ ორი წერტილი რომლებიც ყველაზე შორსაა ერთმანეთისგან
    # ამ შემთხვევაში (1.0, 1.0) და (5.0, 7.0)
    
    # პირველი ცენტროიდი
    centroids.append(
        Centroid(SAMPLES[LOWEST_SAMPLE_POINT][0], SAMPLES[LOWEST_SAMPLE_POINT][1]))

    # მეორე ცენტროიდი
    centroids.append(
        Centroid(SAMPLES[HIGHEST_SAMPLE_POINT][0], SAMPLES[HIGHEST_SAMPLE_POINT][1]))
    
    # ცენტროიდების ეკრანზე ბეჭდვა
    print("Centroids initialized at:")
    print("(", centroids[0].get_x(), ", ", centroids[0].get_y(), ")")
    print("(", centroids[1].get_x(), ", ", centroids[1].get_y(), ")")
    print()
    return

# წერტილთა ობიექტების ინიციალიზაცია
def initialize_datapoints():
    # DataPoint ობიექტებისათვის წარტილები აღებულია SAMPLE მასივიდან როგორც X და Y კოორდინატები 
    # DataPoint ობიექტები რომლებიც ასოცირდება LOWEST_SAMPLE_POINT და  HIGHEST_SAMPLE_POINT 
    # (ერთმანეთისგან ყველაზე შორს მდევარე წერტილები) მივანიჭოთ თავიდანვე კლასტერის ნომერი

    # ალგორითმი დატრიალდება რამდენი წერტილიცაა სიმრავლეში
    for i in range(TOTAL_DATA):
        # შევქმნათ წერტილის ობიექტი
        newPoint = DataPoint(SAMPLES[i][0], SAMPLES[i][1])
        
        # თუ წერტილი მინიმალური წევირი და მივანიჭოთ მის კლკასტერს (0) რიცხვი
        if(i == LOWEST_SAMPLE_POINT):
            newPoint.set_cluster(0)
        # თუ წერტილი მაქსიმალური წევრი და მივანიჭოთ მის კლკასტერს (1) რიცხვი
        elif(i == HIGHEST_SAMPLE_POINT):
            newPoint.set_cluster(1)
        else:
            newPoint.set_cluster(None)
        
        # დავაგდოთ წერტილი მასივში
        data.append(newPoint)
    
    return

# ევკლიდური მანძილი
def get_distance(dataPointX, dataPointY, centroidX, centroidY):
    # გამოითვლება თითოეული წერტილისთვის რომ მივაკუთვნოთ იგი შესაბამის კლასტერს
    return
    (
     math.sqrt(
        math.pow((centroidY - dataPointY), 2) + 
        math.pow((centroidX - dataPointX), 2))
    )

# ცენტროიდების საშუალოს დათვლა
def recalculate_centroids():
    totalX = 0
    totalY = 0
    totalInCluster = 0
    
    # კლასტერების რაოდენობა მოცემულია თავიდანვე
    # და შესაბამისად მაგდენჯერ დატრიალდება იტერაცია
    for j in range(NUM_CLUSTERS):
        # თითოული წერტილისთვის შესაბამის კლასტერში
        for k in range(len(data)):
            # შესაბამისი X და Y წერტილების ჯამი დავიანგარიშოთ
            if(data[k].get_cluster() == j):
                totalX += data[k].get_x()
                totalY += data[k].get_y()
                totalInCluster += 1
        
        # ამ დროს კლასტერის იტერაცის მთავრდება
        # ითვლება კოორდინატების ჯამი გაყოფილი მათ რაოდენობაზე
        # და შესაბამისად ცენტროიდის კოორდინატები გადაინაცვლებს მიღებულ წერტილში
        if(totalInCluster > 0):
            centroids[j].set_x(totalX / totalInCluster)
            centroids[j].set_y(totalY / totalInCluster)
    
    return

# კლასტერების განახლება
def update_clusters():
    isStillMoving = 0

    # ყველა წერტილისთვის დატრიალდეს იტერაცია    
    for i in range(TOTAL_DATA):
        bestMinimum = BIG_NUMBER # მაქსიმალურად დიდი რიცხვი
        currentCluster = 0
        
        # თითოეული წერტილისთვის 
        for j in range(NUM_CLUSTERS):
            distance = get_distance(data[i].get_x(), data[i].get_y(), centroids[j].get_x(), centroids[j].get_y())
            if(distance < bestMinimum):
                bestMinimum = distance
                currentCluster = j
        
        data[i].set_cluster(currentCluster)
        
        if(data[i].get_cluster() is None or data[i].get_cluster() != currentCluster):
            data[i].set_cluster(currentCluster)
            isStillMoving = 1
    
    return isStillMoving

# k - საშუალო ალგორითმის მთავარი ფუნქცია 
def perform_kmeans():
    # ეს ცვლადი რომ მიიღებს მნიშვნელობა ნულს ალგორითმი გაჩერდება
    isStillMoving = 1
    
    # ცენტროიდების ობიექტების შექმნა და მათი მასივში შეტანა
    initialize_centroids()
    
    # წერტილთა ობიექტების შექმნა და მათI მასივში შეტანა
    initialize_datapoints()
    
    while(isStillMoving):
        # გამოანგარიშება საშუალოების 
        recalculate_centroids()
        # დათვლა კვადრატული სხვაობების ჯამი დათვლა
        # შესაბამისად თუ მიღებული კვადრატული სხვაობების ჯამი ტოლი იქნა წინა იტერაციის 
        # ალგორითმს გავაჩერებთ
        isStillMoving = update_clusters()
    
    return

def print_results():
    for i in range(NUM_CLUSTERS):
        print("Cluster ", i, " includes:")
        for j in range(TOTAL_DATA):
            if(data[j].get_cluster() == i):
                print("(", data[j].get_x(), ", ", data[j].get_y(), ")")
        print()
    
    return

perform_kmeans()
print_results()