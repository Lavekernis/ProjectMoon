# ProjectMoon
1) Praca wykonana nad projektem

Wysyłamy dwie wersje projektu - jedna zrobiona metodą dyskretyzacji, druga za pomocą funkcji odeint.
Ostateczną wersją jest ta w folderze Odeint, pierwszą zrobiliśmy przed konsultacjami, ale po nich zrozumieliśmy, że należy zmienić metodę obliczeń.

2) Obliczanie kąta zderzenia

Przyjęta metoda obliczania kąta zderzenia asteroidy z księżycem zwraca wyłącznie kąty z przedziału <img src="https://render.githubusercontent.com/render/math?math=[0,\pi]">.
Nie jest to jednak problem, ponieważ daje nam to obraz tego, ile asteroid pada na którą stronę księżyca
i w jakim rozkładzie (kąty z przedziału <img src="https://render.githubusercontent.com/render/math?math=[\pi/2,\pi]"> reprezentują ciemną stronę księżyca).


3) Problem z działaniem symulacji

Program nie działa dla dużych czasów (>4000 h) i dużej liczby asteroid,
ponieważ funkcja odeint zwraca błąd: 'Excess work done on this call (perhaps wrong Dfun type).'
Możliwe że jest to wynik ograniczeń funkcji odeint, aby temu zaradzić wystarczy startować
więcej symulacji z dużym czasem trwania, ale małą liczbą asteroid (kosztem czasu działania programu).

4) Czy program działa?

Prawdopodobnie tak - na załączonych grafikach widzimy przewidziane przez symulację trajektorie,
które zgadzają się z przewidywaniami teoretycznymi. Nie zaobserwowaliśmy jeszcze asteroidy uderzającej
w księżyc, jednak przy umieszczeniu testowej asteroidy w księżycu program wykrywa ją
i poprawnie oblicza kąt.


![asdasd](https://github.com/Lavekernis/ProjectMoon/blob/master/Figure_2.png?raw=true)

Rysunek trojektorii Ziemi wraz z Księżycem (kolor czerowny i niebieski) oraz dwoma asteroidami.  
![asdasd](https://github.com/Lavekernis/ProjectMoon/blob/master/Figure_1.png?raw=true)

Wykres wielkości składowej x oraz y prędkości Ziemi i Księżyca, dla kolejnych czasów.
