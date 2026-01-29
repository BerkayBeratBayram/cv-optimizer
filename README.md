# CV Optimizer

Benim projem: CV Optimizer. Bu repo, iş ilanları ile özgeçmişleri karşılaştırıp; uygunluk analizi, anahtar kelime çıkarımı ve örnek ön yazı (cover letter) üretimi yapmayı amaçlar. Aşağıda projeyi, kullandığım bileşenleri ve mevcut durumunu özetliyorum.

**Ne yapıyor**
- İş ilanı ile tek veya birden fazla özgeçmiş arasındaki eşleşmeleri vurgular.
- Metin parçalarını (CV / ilan) vektörlere dönüştürerek benzerlik araması (RAG-benzeri yaklaşım) yapar.
- Özet, anahtar kelime çıkarımı ve cover letter taslağı üretir.

**Kullandığım teknolojiler & rollerim**
- **Python 3.12 (tercih edilen geliştirme ortamı)**: Proje geliştirmesi ve paket uyumluluğu için kullandığım sürüm.
- **Streamlit**: Kullanıcı arayüzü (tek sayfa, yükleme ve sonuç gösterimi).
- **ChromaDB**: Vektör tabanlı arama/depolama (retrieval) için kullandığım hafif veri deposu.
- **Ollama**: Yerel LLM istemci arayüzü — analiz ve ön yazı üretimi için model çağrıları bu katmandan yapılır.
- **sentence-transformers**: Metinleri gömme (embedding) formatına dönüştürmek için.
- **pypdf / python-docx**: PDF ve DOCX formatlı CV/ilan dosyalarını okumak için.
- **Basit metin bölücü (simple_text_splitter)**: Uzun metinleri parçalara ayırarak vektörleştirmeye uygun hale getiririm (langchain bağımlılığı kaldırıldı; sadece gerekli basit bölme mantığı kullanılıyor).

**Mimari (kısa)**
- Yüklenen CV/ilan -> metin çıkarımı -> metin parçalama -> embedding -> ChromaDB'e ekleme.
- Sorgu/analiz gerektiğinde uygun parçalar ChromaDB'den çekilir ve Ollama'ya analiz/üretim için gönderilir.

**Depodaki önemli dosyalar**
- [cv_optimizer_app.py](cv_optimizer_app.py): Streamlit arayüzü ve ana iş akışı burada yer alır.
- [cv_optimizer.ipynb](cv_optimizer.ipynb): Geliştirme notlarım, denemeler ve orijinal çalışma notebook'u.
- [requirements.txt](requirements.txt): Projede kullandığım ana Python paketleri (listeleme amaçlı).

**Mevcut durum**
- Uygulama Streamlit tabanlı olarak çalışır hâlde; Python 3.12 tabanlı bir sanal ortam (benim geliştirme ortamım) kullanılarak test edildi.
- ChromaDB ile embedding+retrieval akışı ve Ollama ile üretim entegrasyonu uygulanmış durumda.
- Bazı geliştirme kısımları (ör. çoklu CV toplu işleme arayüzü veya daha kapsamlı hata yönetimi) istenirse genişletilebilir.

**Notlar / politika**
- README, doğrudan çalışma/kurulum komutları veya "şunu şunu yapın" tarzı yönergeler içermez; amacım projeyi ve kullandıklarımı açıkça anlatmak.

İsterseniz bu değişikliği commit edip remote'a pushlayabilirim; onay verirseniz bir sonraki adımı ben yaparım.

Projede neler var

- `cv_optimizer_app.py` — Streamlit tabanlı web uygulaması. PDF veya TXT formatında CV ve iş ilanı yükleyip anahtar kelime analizleri, basit bir semantic retrieval (ChromaDB) ve Ollama ile ön yazı üretimi yapabiliyor.
- `cv_optimizer.ipynb` — Geliştirme aşamasında kullandığım not defteri; veri keşfi, yardımcı fonksiyonlar ve deneyler burada.
- `data/` — (isteğe bağlı) örnek CV veya iş ilanlarını koymak için klasör.
- `requirements.txt` — projeyi çalıştırmak için gereken paketlerin listesi.
- `.gitignore` — sanal ortamlar ve geçici dosyalar için önerilen ignore kuralları.

Ben ne yaptım / neden burada

- Notebook içindeki interaktif menüyü Streamlit uygulamasına taşıdım.
- Metin parçalama (chunking) için gereksiz bir büyük bağımlılığa girmemek adına basit ve güvenilir bir splitter ekledim.
- CV ve iş ilanı metinlerini parçalayıp ChromaDB'ye ekleyerek semantic arama yapılmasını sağladım (ChromaDB kuruluysa çalışır).
- Ollama kullanarak (lokal model) CV ile iş ilanı arasında daha zengin analizler ve ön yazı taslağı üretebilme özelliği ekledim.
- PDF/TXT okuma ve metin kodlama sorunlarını düzelttim, uygulamayı daha sağlam hale getirdim.

Hızlı başlangıç (lokal)

1. Python 3.12 kurulu olması tavsiye edilir.
2. Proje klasöründe sanal ortam oluşturup aktif edin (Windows PowerShell örneği):

```powershell
py -3.12 -m venv venv
& .\venv\Scripts\Activate.ps1
python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt
```

3. Uygulamayı çalıştırın:

```powershell
python -m streamlit run cv_optimizer_app.py
```

4. Tarayıcıda Streamlit'in verdiği yerel adresi açın (genellikle `http://localhost:8501`).

Notlar

- ChromaDB bazı sistemlerde (özellikle Windows) ek build araçları gerektirebilir; bu durumda alternatif olarak basit in-memory yöntemlerle de çalıştırabilirsiniz.
- Ollama çağrıları (`ollama.generate`) için bilgisayarınızda Ollama ve uygun bir model yüklü olmalıdır.

GitHub'a yüklemek

Ben bu repository'ye pushladım; isterseniz siz de lokalinizde aynı adımları takip ederek çalıştırabilirsiniz. Eğer başka bir düzenleme veya ek açıklama istiyorsanız söyleyin, ben güncelleyeyim ve tekrar pushlayayım.

Gelecek planları (opsiyonel)

- `data/` içine örnek CV ve iş ilanı ekleyerek deneme kolaylığı sağlayabilirim.
- Anahtar kelime çıkarımı ve eşleştirme için daha iyi testler ekleyebilirim.
- ChromaDB kurulumunu atlatmak isteyenler için in-memory fallback seçeneği ekleyebilirim.
