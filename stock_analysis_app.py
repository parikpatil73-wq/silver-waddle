import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import os

Framework for Evaluating Publicly Traded Companies
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- (Any additional imports) ---

# Static weights
weights = {
    'Customer_Value': 0.10,
    'Unit_Economics': 0.15,
    'TAM': 0.10,
    'Competition': 0.10,
    'Risks': 0.15,
    'Valuation_Score': 0.40
}

# Helper functions...
def fetch_current_price(ticker):
    try:
        info = yf.Ticker(ticker).info
        return info.get('regularMarketPrice')
    except Exception:
        return None

def normalize(value, low, high):
    if value is None or np.isnan(value):
        return 50
    return max(0, min(100, (value - low) / (high - low) * 100))

def score_factors_auto(ticker):
    t = yf.Ticker(ticker)
    info = t.info
    pe_ratio = info.get('trailingPE', np.nan)
    pb_ratio = info.get('priceToBook', np.nan)
    gross_margins = info.get('grossMargins', np.nan)
    operating_margins = info.get('operatingMargins', np.nan)
    revenue_growth = info.get('revenueGrowth', np.nan)
    beta = info.get('beta', np.nan)
    customer_value = normalize(gross_margins or 0.3, 0.1, 0.7)
    unit_economics = normalize(operating_margins or 0.2, 0.05, 0.4)
    tam = normalize(revenue_growth or 0.1, -0.1, 0.3)
    competition = 100 - normalize(pb_ratio or 5, 1, 15)
    risks = 100 - normalize(beta or 1.2, 0.5, 2.5)
    valuation_score = 100 - normalize(pe_ratio or 30, 5, 60)
    scores = {
        'Customer_Value': round(customer_value, 1),
        'Unit_Economics': round(unit_economics, 1),
        'TAM': round(tam, 1),
        'Competition': round(competition, 1),
        'Risks': round(risks, 1),
        'Valuation_Score': round(valuation_score, 1),
    }
    return scores

# --- Streamlit App Layout ---

st.title("📊 Stock Fundamentals Analyzer")

ticker = st.text_input('Ticker (e.g., AAPL, TSLA)')
period = st.selectbox('Period (days):', [7, 30, 90, 180, 365], index=2)
run = st.button("Analyze")

if run:
    ticker = ticker.strip().upper()
    if not ticker:
        st.warning("Please enter a ticker.")
    else:
        price = fetch_current_price(ticker)
        if price is None:
            st.error(f"Could not fetch price for {ticker}")
        else:
            try:
                data = yf.Ticker(ticker).history(period=f"{period}d")
                if data.empty:
                    st.error(f"No historical data for {ticker}")
                else:
                    factors = score_factors_auto(ticker)
                    weighted_score = sum(factors[f] * weights[f] for f in weights)
                    intrinsic_value = price * (weighted_score / 100.0)
                    df = pd.DataFrame([{
                        "Ticker": ticker,
                        "Current Price": price,
                        "Intrinsic Value": round(intrinsic_value, 2),
                        "Weighted Score": round(weighted_score, 2),
                        **factors
                    }])
                    st.subheader(f"Results for {ticker}")
                    st.dataframe(df)
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.plot(data.index, data['Close'], label='Close')
                    ax.set_title(f"{ticker} Price (Last {period}d)")
                    st.pyplot(fig)
            except Exception as e:
                st.error(str(e))



 

 

 
Table of Contents
Introduction	5
Chapter One: Customer Value Proposition	7
Chapter Two: Unit Economics	16
Chapter Three: Total Addressable Market	23
Chapter Four: Competition	27
Chapter Five: Risks	36
Chapter Six: Does the Price Offer Good Value?	47
The Algorithm	60
Bibliography	62
Acknowledgments	63
About the Author	64
 
Introduction
Congratulations, you are looking to gain a deeper insight into how to make money in the stock market. Investing has been one of the best ways for individuals and families to build sustainable and long-lasting wealth. Unfortunately, the stock market has also been a place where many have lost a small fortune. Why do some investors generate healthy investment returns, and others are caught holding the bag?
In this book, I will discuss six factors that I believe are fundamental to making money in the stock market. Neglecting any of the factors could be damaging. These factors work together to guide investment decision-making in a dynamic stock market. For instance, regardless of how excellent a business is, paying too high a price for the stock could crush any chance of making a return on your investment. Similarly, neglecting a significant risk could turn a seemingly bargain stock into a total loss in less than a week.
The key is to balance all the critical factors that could impact the company’s stock price over the time you consider holding that investment. This book contains the six factors I consider most vital when buying or selling a stock, how I evaluate companies according to these metrics, and how you can use this framework to make money in the stock market.
I developed this framework after studying countless investment strategies. While I did find excellent ideas, I did not find one comprehensive framework to fit my needs. After creating this framework, I found my investing process significantly improved. I can plug in business characteristics into the model, and it will suggest whether or not it makes a good buy.
Of course, Wall Street does not want you to get your hands on this framework. Rather, they prefer you trust them with your hard-earned money. They make more money if you outsource all investment decision-making to them. If you take ownership of your decisions, you can effectively determine if their financial advice is worth paying for. You may still choose to hire a financial professional, but after reading this book, you will be armed with a framework to judge their performance.
I find trusting Wall Street with my family’s wealth the least productive action I can take. Analysts rarely have the freedom to speak their minds about a stock. If an industry analyst puts a sell rating on a stock, the analyst risks losing access to that company’s management team. With less access, the analyst gets less information and is trusted less because investors perceive analysts with proximity to the C-suite as more knowledgeable. Worse yet, some analysts are threatened by losing their jobs if they issue a poor rating. It’s no wonder that most stocks are rated as a buy, and a significantly lower percentage are rated as a sell.
I could go on for several pages about why blindly listening to Wall Street recommendations is a terrible idea, but I won’t. Instead, I will share with you how I took responsibility for my investments and created a framework I use to make decisions.
For those still wondering if investing in the stock market is worthwhile, consider this fact: historically, the average annual return for the U.S. stock market over the last 100 years has
 
been approximately 10%. This figure considers the performance of major stock market indices, such as the S&P 500, representing a broad cross-section of U.S. stocks.
It's worth mentioning that the 10% average return is a historical average and should not be interpreted as a guarantee or predictor of future market performance. Market conditions, economic factors, and other variables can impact investment returns, and individual stock or portfolio performance may differ from the overall market average. Investors should exercise caution, conduct thorough research, and consider their risk tolerance and goals when making investment decisions.
Now for the good stuff: earning an average of 10% return on investment can lead to incredible gains. If you invested in the stock market for 40 years and earned an average of 10%, a $1,000 investment would be worth $45,259. Still more incredibly, if you added an annual investment of $1,000 to your starting balance of $1,000, your investment after 40 years would be worth $487,851.
 
Chapter One: The Customer Value Proposition

It all starts with a product or service. What value is the business providing to its customers?
Case study: It’s critical to consider what needs the business is filling. The Walt Disney Company’s theme parks serve the need for family entertainment. It offers multiple experiences based on fictional characters it has spent decades developing on the big screen and its numerous TV channels.
Disney has delighted families so much that they are willing to pay premium prices to attend its theme parks. Moreover, many kids who visit the parks return as adults to bring their children. It’s common to see three or four generations of Disney Park customers in attendance. Admittedly, attendance at a Disney theme park can be pricey. However, if you have young children, you will find the experience unrivaled.
Disney has over-delivered so frequently that it can ask for premium prices that customers are willing to pay, as evidenced by the crowded attractions, $82.7 billion in revenue in the pandemic-plagued fiscal year of 2022, and $6.8 billion in operating income.
Companies that keep customers coming back have multiple advantages. First, it increases the lifetime value of a customer. Depending on the customer's age, she could be worth 20x, 40x, or 100x of the first purchase. Let’s say the first purchase a person makes is $20. Using the 100x example, that buyer’s lifetime value would be worth $2,000 to the company. When the business looks to buy advertising for customer acquisition, it can spend up to $1,999 to acquire that customer. That example ignored profit margins and the time value of money for simplification.
Moreover, high customer loyalty reduces advertising needs. Delighted customers likely become brand ambassadors, sharing stories about how great your company’s products and services are. This organic recognition is superior to marketing campaigns, sometimes viewed as obviously biased. If your father, mother, brother, sister, cousin, friend, or coworker is to suggest a company to you, that is more likely to result in a purchase than if you see a national television advertisement or an influencer hawking an item on Instagram.
It doesn’t end there. Loyal customers help protect a company’s profit margins by giving it pricing power. As I author this book in 2024, the U.S. is experiencing inflation, raising the cost of living and pressuring enterprise profit margins. The businesses that have increased profits despite the rising costs have been those with pricing power. Coca-Cola and PepsiCo have not been immune to the increasing costs of goods. However, their strong customer loyalty has allowed them to increase prices on their portfolio of beverages and snacks to make up for the higher input prices.
I will end with one final benefit: The better the customer feels about a business's value proposition, the harder it will be for competitors to make inroads. Tesla, Carvana, and CarMax have each taken a significant market share in car sales because they attacked an area where
 
customers felt they were getting little value. You can scarcely find a satisfied individual who purchased a car from a dealership. I have met a few, but they are rare indeed. The sleazy salesman, the lack of transparency on price, and the haggling are despised by most buyers.
Dealerships have survived due to the unique relationships they have with manufacturers. In the United States, state laws known as franchise laws govern the relationship between car manufacturers and dealerships. These laws typically protect the rights of existing dealerships and impose restrictions on manufacturers when establishing new dealerships or terminating existing ones. The specifics of these laws can vary by state. Dealerships overplayed their hand, thinking these circumstances would allow them to mistreat customers while maintaining sales.


By asking probing questions, they identify the maximum price someone is willing to pay.
That practice leaves little consumer surplus, and the person who experienced the salesman extracting maximum value feels unsatisfied. More than anything, this practice has led to the demise of legacy automakers.
That’s why CarMax, with its no-haggle, transparent pricing, has done so well in the used car market. Similarly, Tesla has gained traction with its direct-to-consumer strategy, which skips middleman car dealerships. If car dealerships were not laser-focused on squeezing the highest possible sales price from each car sale and spent more effort on the customer buying experience, they would not be open to such encroachment from competition.
The return and warranty policy is another critical component of the customer value proposition. If you are confident the company will grant you a refund when unsatisfied with a product or service, you are more likely to purchase. Those moments when you hesitate before buying, you can remember that the company has always granted your refund request, so you can comfortably buy knowing that if you want to return, no questions will be asked.
Some businesses have created an automated policy on their websites. This saves the business money because customer service agents do not need to deal with return requests. It also improves the customer value proposition because customers quickly get their refunds approved. Of course, companies place algorithms to detect customers who abuse these policies, but for the most part, it works advantageously.
 
Furthermore, brand power goes a long way to encouraging customers to buy. For instance, recall a brand you have purchased multiple products from and consistently been satisfied with. Let’s say this brand introduces a product in a new category. You are more likely to try out this product from the brand, giving it a greater ability to expand into new categories. Companies with strong brand recognition make for better investments.
Convenience is another vital component to consider. Human nature is always striving for easier ways of doing things. If a company’s products or services offer significant convenience advantages, I would place a greater likelihood of that company’s success. Investors are sometimes surprised at the prices people are willing to pay for convenience. Amazon exists for convenience. You no longer have to drive to a store. Amazon will bring you virtually anything you want to your doorstep in days or hours for some items.
Lastly, companies are now in danger of over-automating their customer service. As many times as I have tried, I have never been able to reach a customer service representative at Microsoft. When it came time to upgrade my computer, I finally switched to Apple. Again, this is a case where Microsoft is overestimating its market power. The company thinks it can add a few percentage points to the bottom line by reducing spending on customer service. However, customer dissatisfaction will open the door for competitors to take market share.


How can an investor measure the customer value proposition?
Now that we have established the importance of the customer value proposition, the next step is to identify the methods for analyzing this critical factor. Of the three methods I suggest, the first is the most important. Personal experiences should be your highest ranked when considering the customer value proposition.
What did you think about the value of the money you spent? Did you feel satisfied with your experience? Would you go back to that company to buy the same thing? Would you try a different item from the company because the first one you tried was so impressive? If you were satisfied with the purchase, how much more would you be willing to pay the next time you return? Was there a difference between what you were willing to pay and what you paid? If so, that means you captured consumer surplus.
If you are reading this book, you are probably a prudent manager of your family’s finances. Otherwise, you would not have money to invest in the stock market. Given that fact, you are likely an excellent judge of the customer value a company offers. My job as a college professor has given me the fortune to talk to many youths about the stock market. One of the most common advice I give students is to do their research and trust their judgment.
Consequently, one of the biggest mistakes I observe investors making is blindly trusting a recommendation from an individual they see on YouTube, TikTok, or Instagram. Sadly, many students have told me how much money they lost by listening to people hyping up meme stocks like AMC Entertainment Group and GameStop. Looking at these companies with a personal lens would reveal their poor prospects.
 
Taking a family of four to AMC for a movie with popcorn, soda, and parking will easily cost me $100. To make matters worse, the movie times are listed as 20 minutes before the movie starts. This is a sneaky way the theatres get you to watch 20 minutes of advertising. All the while, these theatres have been selling $9 popcorn and $7 soda and have made almost zero upgrades to the viewing experience. I could subscribe to several streaming services for less than the price of one movie ticket. Unsurprisingly, movie ticket sales have declined steadily for two decades. According to Statista, movie tickets sold in the U.S. and Canada decreased from 1.575 billion in 2002 to 1.228 billion in 2019. That’s not even including the impact of the pandemic.
Movie ticket sales fell to 825 million in 2023. Meanwhile, AMC is saddled with $4.2 billion in debt as of June 30, 2024, has lost money on the bottom line in seven out of the last eight years, and has diluted shareholders significantly in that time.
Still, people fell for the trap set by unethical influencers who found an opportunity to make money by promising quick and easy profits. Even the CEO of AMC, Adam Aaron, was selling much of his investment in AMC stock just as he was encouraging meme stock investors of the excellent prospects of the business.
“Two months ago, more than 85% of my net worth was in AMC stock, and proper estate planning for a 67-year-old suggests I should diversify my assets a bit. But I don't want any of you ever to think that I have anything but full confidence in AMC's future. So I will do so under the auspices of the parameters of what is called a 10b5-1 plan, where I pass off all the share trading control of the shares that I own or I'm granted to an independent third-party bank based on parameters of the plan that I only partially set. The plan would not go into effect until toward year end at the earliest, and only a small percentage of my owned or granted shares could get sold in any one month. And that would then be repeated over a period of at least several months. This way, I really have passed on the decision-making to someone else on this important topic.”

That was the story AMC CEO Adam Aaron told investors in the company’s second quarter conference call in 2021 while he proceeded to sell his shares. AMC’s stock price has been down over 95% since that moment. I wrote dozens of articles warning investors to investigate the company’s prospects and not fall into the trap of herd thinking. Unfortunately, I don’t think very many people listened. Needless to say, it is important to evaluate stocks before buying.
Another similar story is GameStop. The company sells physical copies of video games when consumers prefer digital copies. Why would you travel to a GameStop location to buy a video game copy when you can access a copy online within minutes? To make matters worse, the price is trending lower online. Game creators and manufacturers can make more money and reduce the risks of inventory obsolescence by selling digital copies. They encourage consumers to switch to digital purchases by making digital-only consoles. Amid this backdrop, GameStop has been bleeding money. Between 2015 and 2019, its revenue fell from $9.3 billion to $8.3
 
billion. Earnings per share fell from $0.87 to negative $1.65. Yet, swindlers found a story they could sell to people to get them to buy GameStop stock. In what world does GameStop have good prospects? Maybe in 1990. Admittedly, physical game copies are still desirable for gamers who wish to trade those copies to recoup some value when they no longer want to play that game. However, those few customers are not enough to support a business the size of GameStop.
Would you purchase these companies’ stocks if you considered the customer value proposition? It’s unlikely. Investors who lacked confidence in their ability trusted storytellers with their money. The result was tragic. People lost their life savings, retirements were delayed, and many had to file for bankruptcy as they borrowed to buy these stocks. As of this writing, GameStop stock is down 77% off its high. AMC stock is down 98%.
My mission is to empower investors to make their own decisions. By researching yourself, you will avoid these swindlers that seem to rise in every generation with a new “sure thing.” There are no guarantees when investing; anyone who promises you a guaranteed return is likely a crook or ignorant. Either way, these are not people to trust with your money.
The second way to measure a company’s perceived value is to look at its historical revenue growth going back five to ten years. You can go back further if data is available. When considering a company’s sales, you want to look for growth: Is it growing, and by how much? Is it growing faster than rivals in the industry? Do you see any year or quarter that seems out of sorts with the rest of the data?
One reason it’s essential to consider the company’s growth against rivals is to dilute the impact of industry growth. What you’re trying to measure is customer value. Sometimes, an industry grows so rapidly that nearly all businesses experience growth. If the company you are evaluating is growing revenue faster than any competitor, it’s likely offering customers the best value.
Remember that consumers place value on several things when making a purchase. Some might place a greater value on convenience. Indeed, the ability to buy a product at several nearby locations is preferred. Selection is another differentiator. If a business only offers one color and three sizes, it’s less desirable than a brand that offers five colors and six sizes.
Similarly, all else being equal, a customer would prefer a lower price. A large cohort of buyers makes decisions based on price. They need a pair of rain boots for their kids. They walk down the aisle at their local Walmart and pick the lowest-priced pair in their kids’ shoe size.
That’s it. No consideration is made to color, style, or brand.
Being the low-cost provider in an industry naturally generates goodwill with consumers.
Of the various strategies a business can employ, the low-cost position is arguably the most difficult to achieve. However, the strategy could also generate the longest-lasting competitive advantage. Offering the lowest prices sustainably requires excellent planning and execution.
Management needs to plan operations to keep costs low. Expenses need tight management to sell products at the lowest prices and still earn a profit. At times, you will see businesses offering their products at prices below their costs, leading to losses on the bottom
 
line. This, of course, is unsustainable. Eventually, this business will need to lower costs, raise prices, or both. Otherwise, it will run out of cash and find few banks or investors willing to fund their losses indefinitely.
Growth companies may sell their products below cost to expand their market share, aiming to scale quickly and outpace competitors. This strategy also helps with customer acquisition, bringing in new users who might generate long-term revenue through repeat purchases or upselling. In industries that rely on network effects, such as tech platforms, pricing below cost can help achieve a critical mass of users, increasing the product’s overall value.
Aggressive pricing can also create barriers to entry, discouraging competitors from entering the market. Lastly, selling at a loss can build brand awareness and customer loyalty, positioning the company as a market leader. That being said, it is up to you to determine the likelihood that a company’s strategy of selling below cost will lead to eventual profitability.
Before completing this section on sales growth, I will touch on outliers and how to deal with them. For instance, you will find an anomaly if you look at Chipotle’s sales figures between 2010 and 2019. Revenue was growing nicely before suddenly falling by 13.3% in 2016. It should immediately indicate that further analysis is needed whenever you notice something like this.
Make a note to yourself to dig deeper into the cause.
In Chipotle’s case, a terrible food virus outbreak affected many of its customers. My wife and I were unfortunate enough to eat at Chipotle while on vacation during this outbreak. We were sick all week, and it ruined our trip. Before this incident, we ate at Chipotle once or twice a month. After the event, we never went back.
The point I am trying to make with that story is that irregular fluctuations in revenue could be a clue to something much bigger. An event like Chipotle’s experience can do irreparable damage to customer loyalty. Regardless of how many commercials Chipotle runs or how much it lowers prices, they might never count us as customers again. Every time I think of Chipotle, I get an uncomfortable feeling in my stomach. Even writing about it reminds me of the time I got sick.
Perhaps I have unfairly singled out Chipotle because of my experience, but it is certainly not alone in losing customer trust. You might remember Toyota’s acceleration issues leading to car accidents, British Petroleum’s Horizon underwater oil well disaster, Wells Fargo, and the account creation fiasco. Undoubtedly, these events impacted some people who have vowed never to do business with any of these companies.
The Toyota acceleration disaster refers to a series of incidents from 2009 to 2010 involving unintended acceleration in Toyota vehicles, leading to several accidents, injuries, and fatalities. Millions of vehicles were recalled globally as drivers reported that their cars accelerated uncontrollably, often linked to faulty floor mats, sticky pedals, or electronic issues. The issue gained widespread attention after high-profile accidents and investigations by regulators, with Toyota eventually paying billions in fines and settlements. The crisis severely damaged Toyota's reputation for safety and reliability, prompting significant changes in quality control and safety protocols.
 
The BP underwater oil disaster, also known as the Deepwater Horizon oil spill, occurred on April 20, 2010, in the Gulf of Mexico. It was caused by an explosion on the BP-operated Deepwater Horizon drilling rig, which resulted in the release of nearly 4.9 million barrels of oil into the ocean over 87 days. This became the largest marine oil spill in history. The disaster caused widespread environmental damage, killing marine life, polluting coastlines, and disrupting local economies dependent on fishing and tourism. BP faced massive legal, financial, and reputational consequences, including billions in fines and compensation.
The Wells Fargo fake accounts scandal emerged in 2016 when it was revealed that the bank's employees had opened millions of unauthorized bank and credit card accounts without customers' consent. Under intense sales pressure and unrealistic performance targets, employees created these accounts to meet quotas, leading to fraudulent fees and damaging customer credit. The scandal resulted in significant public outrage, regulatory fines totaling billions of dollars, and widespread criticism of Wells Fargo's corporate culture. Top executives resigned, and the bank faced lasting reputational damage, prompting reforms in its sales practices and oversight measures.
Finally, you can check on the customers’ perceived value of a business by looking at its net promoter score. The NPS measures customer loyalty and satisfaction by asking customers to rate their likelihood of recommending a product on a scale of 0-10. Those who rate the product a nine or ten are promoters, seven or eight is considered passive, and six and below are detractors. The Net Promoter Score is calculated by subtracting detractors from promoters. As a result, if a company has more promoters than detractors, the score is positive. A high NPS score, typically ranging from 50 to 100, indicates the following positive aspects about a company:
A high NPS score suggests that customers are generally satisfied with their experience with the company. They will likely be happy with the product or service received and will speak positively about it to others.
Customers with a high NPS score are likelier to become brand advocates and recommend the company to their friends, family, colleagues, or social network. They become voluntary promoters of the brand, helping to attract new customers and contribute to organic growth. Of course, if your customers promote your product, that is free advertising. It is arguably the greatest value advertising because it comes from people outside the company, so it is not likely to be considered marketing by customers.
A high NPS score indicates that customers are likely to share positive experiences with others, either through direct conversations or online platforms such as social media, review sites, or forums. Positive word-of-mouth can significantly enhance a company's reputation and influence the purchasing decisions of potential customers. Tesla has long had one of the highest NPS of any company. It is no coincidence that Tesla also has the smallest advertising budget of any large automaker. The EV pioneer lets its customers do the bragging.
When customers are highly likely to recommend a company, they are more likely to remain loyal and continue doing business with it. This can contribute to higher customer retention rates and reduce customer churn. If someone has been bragging about the quality of his
 
Tesla for years, it will be psychologically challenging for this person to buy any other brand when it is time to replace the older model.
A high NPS score can serve as a competitive advantage for a company. It indicates that the company is performing well in terms of customer satisfaction and loyalty compared to its competitors. Positive word-of-mouth and strong customer advocacy can attract new customers and differentiate the company in a crowded market.
It's important to note that while a high NPS score generally reflects positive customer sentiment and satisfaction, it should be considered in conjunction with other customer feedback metrics and business performance indicators. Additionally, it's essential to regularly monitor and track NPS scores over time to identify trends, address potential issues, and continuously improve customer experiences.
I encourage investors to consider the price to value a business offers vis-à-vis its competitors. An interesting example in this analysis is Netflix. How much quality content do streamers get with a Netflix subscription? How does that compare to its rivals? This is another way of getting into a customer’s viewpoint. People have choices when they go into the marketplace. It’s important to consider where the prospective company lies in the range of options. With some light research, you can find the various pricing strategies of streaming providers.
A supplemental evaluation to consider in this research is how sustainable the company’s position is. You might offer the best-in-class service at the lowest price, causing you to lose money on the bottom line.
In the previous paragraph, I recommended comparing the price-to-value relationship vis- à-vis competitors. Here, I will recommend the same analysis vis-à-vis substitutes. With Netflix as an example, Hulu would be a competitor, and Spotify would be a substitute. People can watch content for entertainment or listen to podcasts or music. Generally speaking, the more substitutes and competitors a company has, the less price power it commands.
How does Netflix stand in relation to those substitutes like listening to music, going out to a ball game, playing video games, etc.? Investors will be hard-pressed to find a company that offers as many hours of entertainment at the price per hour that Netflix provides. You might argue that Netflix has thousands of hours of unwatchable content, and I would agree with you, I rarely find anything worth watching on Netflix. However, over 200 million Netflix subscribers would disagree with you and me. The sustainability topic will take us into the next chapter on unit economics.
 
Chapter Summary/Key Takeaways
This chapter underscores the importance of customer retention and satisfaction in evaluating a company's performance and potential for long-term success. It uses examples, such as Disney's theme parks and their multigenerational appeal, to highlight how meeting customers' needs can lead to sustained success and premium pricing.
The text emphasizes the advantages of high customer retention, including increased lifetime customer value and reduced reliance on advertising, as delighted customers become organic brand ambassadors. The chapter also explores how loyal customers contribute to a company's pricing power and protect profit margins, particularly during economic challenges like inflation.
Furthermore, the discussion touches on the significance of the customer value proposition, considering factors such as return policies, brand power, and convenience. It highlights that a company's ability to offer value can influence customer loyalty, brand perception, and resistance to competitive pressures.
The text then shifts to guiding investors on how to measure a company's customer value proposition. It suggests three methods: personal experiences, historical revenue growth compared to competitors, and the Net Promoter Score (NPS). It encourages investors to trust their judgment, analyze historical growth trends, and consider the NPS as an indicator of customer satisfaction and loyalty.
The chapter concludes with a call for investors to evaluate a company’s price-to-value relationship compared to competitors and substitutes, considering sustainability and the company's position in the marketplace. The Netflix example illustrates the importance of understanding how a company compares to substitutes and competitors in providing value to customers.
 
Chapter Two: Unit Economics
Imagine a business that offers you excellent content for free. Let’s also assume you don’t have to watch any advertising. A service that aggregates the best movies, shows, sports, and news from all the studios worldwide. You would be fond of this product, give it high survey scores, use it often, and tell your friends, family, and colleagues about this fantastic service.
However, without ad revenue or subscription fees, this business would likely lose tremendous sums of money on the bottom line and likely go out of business or change its business model. That’s why this chapter is so important. It’s easy to generate high customer value scores while losing money on the bottom line. The difficulty is in serving customers well while earning reasonable profits. That takes skill, hard work, and imagination.
Analyzing unit economics allows businesses to determine whether each unit sold generates a profit or loss. Companies can assess the profitability of their core operations by calculating the revenue per unit and subtracting the associated costs (including direct costs such as production, marketing, and distribution). This information is essential for making informed pricing, cost management, and resource allocation decisions.
Often, companies suggest they only lose money on sales because they are trying to get big fast. There are valid arguments for this strategy. We talked about some of these examples in the previous chapter. Specific industries have characteristics that are likely to result in winner- take-most market share. It might be prudent to absorb losses while growing at a blistering pace to capture most of the market before competitors can establish themselves.
Then, with competition out of the way, the company can raise prices, cut costs, and focus on profitability. As you might imagine, this is a risky strategy. If it works, it can yield massive returns on invested capital. As an investor, you take a home run swing when buying stocks with this strategy.
Furthermore, some management teams will try to convince investors they are not profitable because they are establishing economies of scale. Investors should take these arguments with caution. Unless you can identify specific ways the company will lower costs per unit on a larger scale, take a wait-and-see approach to forecasts of expanded profit margins.
For instance, advertising is one proven industry that delivers lower costs on a larger scale.
Marketers pay a higher price for advertising if they purchase ads for a local market like Miami, Florida. However, if they buy ads from the same supplier on a national scale, they are likely to receive better rates.
If the unit economics are positive, the business has a strong foundation for profitability and can generate sustainable returns. Conversely, unfavorable unit economics indicate potential issues and the need for adjustments to pricing, cost structure, or operational efficiency.
Unit economics provides insights into a business's ability to scale its operations. If the unit economics are favorable, scaling the company would increase revenue and profitability. However, if the unit economics are unfavorable, scaling the business could exacerbate losses and
 
financial challenges. If you’re making $1/unit at 100 units, that would be $100 profit. At 1,000 units, that would be $1,000 in profits.
Consider the opposite. At a $1 loss per unit, the more units you sell, the more money you lose. Such a business is better off working to improve the unit economics rather than trying to grow the business. Sadly, many companies in this unfortunate situation decide to grow instead. They then try to convince investors to buy the stock because of its excellent growth potential. In these cases, the unsuspecting investors are the customers. The company may never reach profitability, but it can continue asking investors for more money to pay the management team’s salary and lavish lifestyle. Understanding the scalability potential based on unit economics will protect you from investing in these schemes.
By understanding unit economics, businesses can allocate their resources effectively. They can identify areas with strong unit economics that deserve more investment and focus. Conversely, they can identify areas with weak unit economics that may require adjustments or strategic considerations.
Unit economics is crucial in attracting investors and securing funding. Investors evaluate businesses’ financial viability and potential return on investment. Positive unit economics demonstrate that the company has a clear path to profitability and sustainable growth, making it more attractive to potential investors. If you demonstrate favorable unit economics on a smaller scale and want money to expand, investors will be more likely to grant you the funds needed.
Monitoring unit economics allows businesses to identify areas of concern or underperformance promptly. If unit economics are not meeting expectations or are trending negatively, it signals the need for corrective actions. This could involve optimizing costs, refining pricing strategies, improving operational efficiency, or revisiting the business model.
Unit economics provides critical insights into a business's profitability, scalability, and financial health. Analyzing and optimizing unit economics allows businesses to make informed decisions, attract investors, and drive sustainable growth. Companies can build a solid foundation for long-term success by focusing on unit-level profitability.
One of the best ways to expand profit margins is through economies of scale. Businesses can establish economies of scale by implementing strategies and practices that enable them to achieve cost advantages and increase efficiency as their scale of operations expands. Here are several ways businesses can establish economies of scale:
Increased production volume: As a business produces and sells more units of a product or service, it can spread its fixed costs (e.g., manufacturing equipment, facilities, research and development) over a larger output. This reduces the cost per unit, leading to economies of scale.
One of the best examples of costs being spread among more customers is Netflix. The streaming pioneer pays the same price to create content whether 1,000 people or 10 million people watch it. Spreading the cost of a movie or series across 1,000 people will lead to a much greater cost per customer than it would if you spread that across 1 million people. Because of this
 
characteristic, Netflix has the potential to expand profits and cash flow relatively better than a business without this ability.
This feature is generally found in businesses with low variable costs per unit. This is another way of saying the company’s costs do not rise with each new customer. A software company will have low variable unit costs. The code has already been written. A new customer merely gets access to something that’s already been created. A car company will have high variable costs. Each new customer must have a car built. If a car company wants another customer, it has to make another car. For this reason, specific industries are better suited for higher profit margins. A car manufacturer will never have the margin potential of a software company.
Bulk purchasing and negotiation power: larger businesses can leverage their size to negotiate better deals with suppliers, secure discounts on raw materials, and reduce procurement costs. Bulk purchasing benefits businesses from lower unit costs, reducing overall expenses.
Improved operational efficiency: With more extensive operations, businesses can invest in advanced technologies, production systems, and automated processes, which enhance productivity and reduce labor and overhead costs. Streamlining processes, implementing lean manufacturing, and optimizing supply chains help drive efficiency gains.
Specialization and division of labor: As businesses grow, they can divide tasks and responsibilities into specialized roles, allowing employees to focus on specific areas of expertise. In a small business, an employee may answer phone calls, manage social media, and do bookkeeping. The company can hire one person for each role as it gets bigger. Specialization leads to increased efficiency and productivity, reducing costs per unit.
Enhanced bargaining power with customers: Larger businesses often have more influence in negotiating contracts and pricing with customers. They can offer volume discounts, secure long-term contracts, or demand favorable terms, providing a competitive advantage over smaller competitors.
Research and development advantages: Businesses with larger resources can invest more in research and development (R&D), enabling them to innovate, develop new products, or improve existing ones. This can lead to cost savings, increased product quality, or differentiation in the market.
Marketing and advertising efficiency: A larger business can benefit from economies of scale in marketing and advertising by spreading the costs of campaigns and promotional activities over a larger customer base. It can negotiate better rates with media outlets or invest in more effective marketing strategies. Recall earlier that a business can get better terms from media outlets when purchasing national advertising.
Geographic expansion: Expanding into new markets or regions allows businesses to capture a more extensive customer base and spread fixed costs over a broader revenue stream. This can increase economies of scale by achieving higher sales volumes and better resource utilization.
 
It's important to note that achieving economies of scale requires careful planning, investment, and effective management. Businesses must balance the benefits of scaling operations with potential challenges, such as increased complexity, coordination issues, and potential diseconomies of scale.
Economies in scale allow a business to generate expanding profits as sales grow. With sales of $1,000, it generates $100 in profit. When sales grow to $2,000, profits increase to $300. Notice how profits tripled while sales doubled. That’s usually evidence of economies of scale. That said, this feature can sometimes be purposefully built into a business.
For instance, let’s say you run a barbershop. You can pay the barbers a fixed salary of
$4,000 per month. Regardless of sales in a given month, they will earn $4,000 per month. That would increase profits when sales are booming because the barber’s salary will stay the same. For instance, at $5,000 in monthly sales, the profits will be $1,000. At $10,000 in sales, profits will be $6,000. Notice how sales increased by $5,000 and profits increased by $5,000. That’s because you chose to pay the barber a fixed salary. In the above example, you’re probably patting yourself on the back for this choice.
However, there is a downside to that strategy. You may have already guessed it. If the business suffers a dry spell and sales fall, the profits will fall even further because the salaries don’t change. With $2,000 in sales, the company will suffer a $2,000 loss because you still have to pay the barber a fixed salary of $4,000. If sales fall further to $1,000, the business will lose
$3,000. Now you are not so happy with your choice of a fixed salary. You are kicking yourself for not hiring the barber on commission.
An alternative could be to offer barbers a commission-based job, whereby the barber earns 50% of each haircut completed. In this case, when sales increase, the profits will not grow as much because you will share the upside with the barber. The benefit is that if sales decrease, your expenses will also decrease, lessening the impact of downturns. In the upside scenario, with sales of $10,000, profits will be $5,000 instead of $6,000. In the downside scenario of sales falling to $1,000, profits will be $500 instead of a loss of $3,000.
Does the business make money each time it sells a widget or renders a service?
This can sometimes be a simple observation. If you look at a company’s income statement, you will often see sales and costs of goods sold as the first two items, followed by gross profit, which is simply sales minus the cost of goods sold. When a company’s sales are larger than its cost of goods, it typically profits from each sale.
In other words, for a merchandiser, it means buying an item for $5 and selling it for more. For a manufacturer, it means it costs the company $5 to make, and it sells it for more. At the very least, you want companies with good unit economics. It demonstrates that management is good at doing whatever the company is doing.
It’s easy for investors to get excited about a stock growing rapidly with innovative products. However, a quick look under the hood reveals that many of these businesses are selling products at prices way below their costs. Of course, customers are flocking to buy the product.
 
When this company finally runs out of capital and needs to raise prices, it quickly finds customers fleeing to its more established competitors or new rivals at lower prices.
Sometimes, businesses employ this strategy of selling below costs to expand to a larger scale where they are confident they can lower costs and become profitable. Let’s say your supplier is willing to sell you sweaters for $4 a piece if you buy 1,000 units monthly but will sell you at $2 a piece at 5,000. In that case, there is a clear path to profitability by selling shirts initially at a loss of $3 each. Investors should identify this opportunity is feasible for the company operating at a loss before becoming convinced profitability will magically manifest. In other words, evaluate the business model to determine if you can reasonably expect the company to demonstrate profits at a larger scale.
That doesn’t mean you should never invest in growth stocks that are losing money.
However, it requires an adaptation of the unit economics considerations. In this case, you look for a gross profit margin that improves as the company grows in sales. That could mean it had a gross margin of -35% on sales of $3 million. And the following year, a gross margin of -28% on sales of $5 million. The year after that, a gross margin of -15% on sales of $7 million. It is our job as investors to determine if this improving profit margin is sustainable.
This demonstrates that the business has economies of scale. Perhaps its suppliers lower the price per unit when they buy in higher quantities. Or maybe they utilize a more significant percentage of its manufacturing facilities with more sales. In my experience, it’s usually a combination of factors that causes gross margins to expand with rising sales. Reading a company’s annual report will usually reveal why the margins are improving.
Interestingly, there can be a tradeoff between profit margins and revenue growth. Intuitively, it makes sense. A business that sells products at lower prices will attract more customers and repeat purchases. A prime example of these two approaches can be observed between Costco and Target. Costco runs on a membership model where folks pay an annual fee to shop in warehouses. In return, Costco’s merchandisers secure good prices for relatively fewer items and pass those savings to customers. Costco relies on high-volume sales to large quantities of customers to make up for the smaller profit margins.
Meanwhile, Target sells products at higher markups, preferring to sell fewer units but make more profit on each unit. The result is as you might imagine. Costco’s gross profit margin averaged 13% between 2014 and 2023. Its operating profit margin averaged 3.2% at that time. Target’s gross profit margin was 29.3%, and operating profit margin was 6.4%. As an added benefit to this strategy, Costco’s inventory turnover ratio, which measures how quickly a merchant sells an item after receiving it, is consistently near twice the rate of Target.


Evaluating profitability in heavy fixed investment businesses
The gross profit margin is easier to evaluate with light fixed-asset businesses, those with a higher percentage of their costs of goods sold as variable costs. It presents a greater challenge when the business makes a large upfront investment and then relies on selling enough units to
 
cover the initial cost and make a profit. For instance, consider Netflix’s business model. The company spent $17.7 billion on content in its fiscal year 2021. Regardless of how many subscribers it has for the year, it has already committed the money.
To judge the unit economics of this business, you would need to look at it holistically.
How many subscribers did it have in the previous year, and how much revenue did it generate? If its revenue in 2020 was only $10 billion, then these are not good unit economics. However, Netflix’s revenue in 2020 was $30 billion, so spending $17.7 billion on content leaves a decent amount of money for other needs. Further, content is a long-lasting asset. It can serve new subscribers for decades. The bigger Netflix’s revenue base gets, the smaller the percentage of that revenue it will need to spend on content.
This example reveals the need to consider the customer or revenue base across which the large upfront investment will be spread. Many software companies promise investors that investments in the near term will lead to massive profits down the road when they achieve a larger scale. Investing in companies at this stage is risky. There is no guarantee they will ever reach a scale to become profitable.
Moreover, there is the risk that once they prove the concept can be profitable, a bigger rival launches its own version and takes a chunk of market share. When investing in these types of companies, look for evidence it’s getting closer to profitability. Are the losses on the bottom line decreasing as revenue is growing? If you can see demonstrable progress on this front, it is a good sign that the business can scale to profits.
Additionally, in these situations, it can be informative to look at the total addressable market, which will be discussed more in the next chapter. If the opportunity is big enough, choosing a high fixed-cost strategy can pay off handsomely.


Chapter Summary/Key Takeaways


The chapter discusses the importance of analyzing unit economics to understand whether a business generates profit or incurs losses. While achieving high customer value scores is easy, sustaining profitability is the real challenge. Unit economics involves calculating revenue per unit and subtracting associated costs to assess the profitability of core operations.
The text explores common arguments businesses make for initial losses, such as rapid growth strategies or establishing economies of scale. It emphasizes the importance of cautious evaluation and identifying specific ways costs will decrease with scale.
Key points regarding unit economics include:
1.	Business Model Validation: Positive unit economics validate the sustainability of a business model, indicating a strong foundation for profitability.
 
2.	Scalability Assessment: Unit economics offers insights into a business's ability to scale operations profitably.
3.	Resource Allocation: Understanding unit economics helps allocate resources effectively, focusing on areas with strong unit economics.
The chapter uses Amazon as an example to highlight the importance of effective capital allocation based on unit economics. Positive unit economics are crucial for attracting investors, and monitoring them allows for prompt course correction if needed.
Economies of scale are discussed as a crucial factor for expanding profit margins. Ways to achieve economies of scale include increased production volume, bulk purchasing, improved operational efficiency, specialization, enhanced bargaining power, research and development, marketing efficiency, and geographic expansion.
The text emphasizes the need for careful planning and effective management to balance the benefits and challenges associated with economies of scale.
The chapter concludes by addressing the trade-off between profit margins and revenue growth, exemplified by Costco and Target’s different strategies. Costco focuses on high-volume sales with lower profit margins, while Target sells fewer units at higher markups.
For businesses with heavy fixed investments, like Netflix, evaluating unit economics requires a holistic approach. The example underscores the importance of considering the customer or revenue base for spreading significant upfront investments and suggests looking for evidence of progress toward profitability when investing in such businesses. Total addressable market size is introduced as a factor in high fixed-cost strategies.
 
Chapter Three: Total Addressable Market
All things being equal, investing in a company with a large addressable market is better. It’s typically more lucrative to be the fourth largest business in a $1 trillion market than boasting the most significant market share in a $20 billion market. Moreover, it leaves greater room to sustain revenue growth.
An even better scenario is to invest in a company with a large and growing market. That way, a company can expand without taking market share. Like riding an escalator, a business rises by standing still. Better yet, a business can grow faster by moving forward and getting help from the escalator.
In a small market, where total customer spending equals $500 million, a fast-growing company will quickly hit the ceiling of revenue growth. If you’re considering investing in a stock that has a market capitalization of $350 million, total revenue of $150 million, and net income of
$25 million in a total addressable market (TAM) of $500 million, there is not much higher that stock can go. The company already has a 30% market share in the example above. It would be difficult for it to gain more share. Without gaining market share, its only hope for increasing revenue would be for growth in the overall market. In the above example, you are relying heavily on industry growth.
One of the primary advantages of investing in companies with a large TAM is the potential for long-term growth and returns. Companies that have a large TAM are often seen as having significant growth potential, as they have a large potential customer base and can expand market share as they capture new customers. This can lead to substantial long-term growth and returns for investors.
For example, a company like Amazon has benefited from having a large TAM. When Amazon first started as an online bookstore, its TAM was limited to the number of people who wanted to buy books online. However, as Amazon expanded its product offerings and entered new markets, its TAM grew significantly. Today, Amazon's TAM is estimated to be in the trillions of dollars, encompassing everything from online retail to cloud computing to entertainment. By investing in companies like Amazon with a large TAM, investors can benefit from this long-term growth potential.
Additionally, in large, growing markets, there is room for segmentation. One company can focus on the North American market, another on the European market, and the next on the Asian market. The regional focus means each company does not need to compete with the other. As you will see in the chapter on competition, it can be devastatingly bad for profits.
Segmentation need not be geographic. Markets can be split into low-price, average, and premium. In this type of split, each business can specialize in serving the needs specific to its customer base. The low-price provider can focus on driving cost-efficiencies, economies of scale, and higher turnover. Meanwhile, the premium provider can look for innovation, strong advertising campaigns, and quality improvements.
 
For instance, the home improvement market in the U.S. is estimated at $900 billion in 2022. The two dominant players in this industry are Home Depot and Lowe’s. The segmentation between these two is focused on the professional versus the do-it-yourself. Home Depot has positioned itself as the favored destination for professionals. An estimated 50% of Home Depot’s sales in 2022 came from professionals. Meanwhile, Lowe’s focuses on the do-it-yourself market.
Between 2014 and 2022, Home Depot’s operating profit increased from $9.2 billion to
$23 billion, and its sales grew from $78.8 billion to $151 billion. Lowe’s, for its part, has seen its operating income increase from $4.1 billion to $12 billion on sales growth from $53.4 billion to
$96.2 billion. It should not be surprising that in that time, Home Depot’s total return to shareholders, including dividends, was 370%, and, coincidentally, Lowe’s was also 370%. Investing in companies operating in large and growing total addressable markets can be lucrative.
In smaller markets, segmentation may not be possible. Each segment has to be large enough to support a business. A smaller overall market leaves smaller segments.
Investing in companies with a large TAM can also help mitigate risk. If a company operates in a large and growing market, it may be less susceptible to economic downturns or market fluctuations. This can help reduce risk and provide some stability to an investor's portfolio.
For example, a company like Apple has a large TAM in the smartphone market. While economic downturns or market fluctuations may affect the overall stock market, the demand for smartphones and other electronic devices is likely to remain relatively stable. This can help mitigate some of the risks associated with investing in the stock market, as the company's revenue and profits may be less susceptible to economic volatility.
Another advantage of investing in companies with a large TAM is the potential for insulation against competition. Companies with a large TAM often have a significant advantage over smaller competitors due to their more considerable resources and ability to scale. This can make it difficult for smaller competitors to enter or gain market share, giving the more prominent company a competitive advantage.
For example, a company like Tesla has a large TAM in the electric vehicle market. While other companies produce electric vehicles, Tesla's significant market share and brand recognition give it a competitive advantage over smaller competitors. As Tesla continues to expand its product offerings and grow its customer base, it may become even more difficult for smaller competitors to enter or gain market share. By investing in companies with a large TAM, investors can benefit from this competitive advantage and potentially higher profitability over the long term.
Perhaps unquantifiable, however not less critical, is how talent is impacted by market opportunity. Running a successful organization requires intelligent, ambitious, and talented people committed to the business. A challenge in companies operating in a smaller total addressable market is the difficulty of attracting and retaining talent.
 
Intelligent workers understand what’s happening within the company and the industry. If they get a whiff that this particular company is approaching a ceiling, they might start looking for opportunities elsewhere. Why would they do this? Well, one of the first things enterprises start doing when they reach a ceiling in terms of total revenues is efficiency improvements.
Those include layoffs, restructuring, and cost-cutting.
If you have reached your ceiling in sales, the focus shifts to growing profits by reducing expenses. Staff reductions are one-way enterprises expand profitability once sales growth has stalled. When growth is robust, management is focused on capturing market share and has less time to work on efficiency. Cost-cutting activities are typically saved for companies that have reached their likely maximum scale.
I should also note that even growth companies sometimes take cost-cutting actions during economic recessions. Still, it is less likely that a business would look to cut costs, even in a recession, if sales increase. Instead, it might view the economic recession as an opportunity to attract talented individuals from companies forced to make layoffs.
Overall, reaching a peak in sales means potential layoffs, fewer opportunities for promotion, and less favorable compensation. Savvy individuals will look to switch to another company as they observe the likelihood of these factors arising. Therefore, a large total addressable market allows a company to attract and retain a greater number of the highest-quality people.
The company’s management team sometimes gives total addressable market data, but not always. Therefore, you may need to look outside the firm to data providers for that information. One of my favorite sources for TAM data is Statista.


Chapter Summary/Key Takeaways
The chapter emphasizes the importance of investing in companies with a large Total Addressable Market (TAM) for several reasons. Firstly, it argues that being part of a vast market is more advantageous than having the largest market share in a smaller market, as it provides more room for sustained revenue growth. The potential for long-term growth and returns is highlighted, with examples like Amazon demonstrating the benefits of expanding within a large TAM.
The chapter also discusses the advantages of investing in companies operating in growing markets, where there is room for segmentation. Segmentation can occur geographically or based on different market segments, allowing businesses to specialize and avoid direct competition.
The example of Home Depot and Lowe's in the home improvement market illustrates how segmentation can lead to success for both companies. Large markets also reduce competitive pressure. Enterprises can grow sales without encroaching on someone else’s market share.
Furthermore, the text suggests that companies in large and growing markets may be more resilient to economic downturns, providing stability for investors.
 
An often overlooked aspect is the impact on talent. Companies operating in smaller markets may struggle to attract and retain skilled individuals, as the growth potential and opportunities for advancement become limited. The chapter concludes by emphasizing that a large TAM allows a company to attract and retain high-quality talent, while smaller markets may lead to efficiency improvements, layoffs, and less favorable conditions for employees.
 
Chapter Four: Competition
Fierce competition among industry participants can be detrimental to profits.
Interestingly, competition can come in many forms. The most obvious is price. One business wants to capture market share, so they undercut the store across the street. Observing the move, the rival fights back with a price cut. Uncontrolled, this usually leads to shrinking profits until one of the companies bows out of the battle. Unfortunately, these battles can last for an extended time. This is especially true if the companies in competition have deep pockets via cash balances and borrowing capacity.
Regardless of who wins the war, the competition will be costly and could take several years to play out. It’s difficult for investors to predict who will win these contests or when they will end in a stalemate. I prefer to avoid these situations altogether. These competitions based on price are so dangerous that they are often a last resort. Businesses know the potential outcomes and are careful not to compete on price.
Businesses, especially larger ones with budgets for economic analysts, spend meaningful time watching their competitors. The data collected informs owners and senior managers on how to respond to competitive actions. Prudent businesses prepare responses ahead of time. For instance, if our rival cuts prices on its main product by 10%, we will cut prices on our main product by 15%. Additionally, we will make it known that our price cut is in response to a competitor’s pricing decision. In that way, a clear message is sent – if you try to gain market share by cutting prices, you will face retaliation. These retaliatory actions are as much intended to send a message as they are to gain market share.
This shifts the decision back to the competitor. Do they cut prices again? Do they make an announcement attempting to cool the rivalry? The back-and-forth will continue until an equilibrium is reached. After years of market competition, businesses train each other on the consequences of competitive actions. The hope is that, like touching fire, the rival will feel the pain and learn not to do it again.
A more common form of competition is through advertising or promotional incentives. In this method of attempting to steal customers, a business increases sales and marketing spending to make its product or service appear more attractive. This is a less damaging form of competition because these offers, commercials, or incentives can be reduced or stopped almost instantly. Reversing multiple rounds of price cuts can be shocking to customers and will likely cause a mass exodus.
One example of this type of competition could be an offer of 25% off a purchase of $100. This might look like a price cut, but it’s better categorized as a promotion or incentive because it can be targeted. A business can choose who receives the coupon. Does it go out to all its customers? Those who have not been to the store in six months? Or those who built a shopping cart online but failed to purchase? Depending on that choice, a rival can respond accordingly. If the offer was geared to previous customers, it may not be considered threatening to take market share. A rival is likely to respond aggressively if the offer is geared to an entire geographic region.
 
An example of fierce competition using promotional activities is happening right now in the food delivery industry in the U.S. DoorDash, Uber Eats, and others are fighting tooth and nail to gain market share in this fast-growing industry. The belief is that there is only room for one or two companies in this market in the long run. Therefore, these companies are investing aggressively, trying to put the rest out of business.
In the last month, I have received promotional offers from four different food delivery companies. These offers include 50% off my order, 40% off my next three orders, and $25 off my order of $40 or more. These offers have been common over the past several years. I rarely use one of these providers unless I have a coupon.
Again, this back-and-forth between competitors squeezes profit margins and reduces trust between industry participants. After all, no business likes it when a rival encroaches on its turf.
Competition shouldn’t be confused with domination. Sometimes, a company comes along with a product or service that is so superior that it proceeds to capture the market.
Given the high variable cost of delivering food, there is likely only room for one or two companies in the long run. In other words, it’s a business that requires a large scale to earn profits. This is an excellent moment to discuss winner-take-all markets again because the food delivery business is a prime example of that type. A winner-take-all market is a market structure in which a small number of firms or individuals capture the majority of market share and profits, leaving little room for competitors. In these markets, a single winner or a few dominant players emerge while the rest of the participants struggle to gain a significant foothold. This phenomenon can occur in various industries and is driven by several factors:
Network Effects: Winner-take-all markets often result from network effects, where the value of a product or service increases as more people use it. Social media platforms like Facebook and communication tools like WhatsApp are classic examples. The more users a platform has, the more valuable it becomes, making it difficult for new entrants to compete.
Would you rather use a social media app with two billion daily active users or one with two thousand? The app with more people is more attractive since the intention is for social interaction.
Economies of Scale: Companies that achieve economies of scale can produce goods or services at lower costs per unit as they expand their operations. This cost advantage can be a barrier to entry for smaller competitors, as they cannot match the pricing or resources of larger firms. A company producing one million widgets can lower the cost of producing each widget by negotiating with suppliers for lower prices because they are buying greater quantities. A rival that only purchases one hundred thousand units may not be able to secure a similar price. The lower cost of goods sold allows the business with the greater scale to sell the product at a lower price than its rival, and therefore achieve greater market share.
Branding and Reputation: Strong branding and a solid reputation can give a company a significant advantage in a winner-take-all market. Consumers often gravitate toward trusted brands, making it challenging for new entrants to gain consumer trust and market share. When you walk down the grocery store's soda aisle, do you notice new brands? Coca-Cola, PepsiCo,
 
and DrPepper have worked diligently to make their brand the only ones most people will consider. The aforementioned brands consistently take considerable market share even though many newer and generic sodas are priced lower and on the same shelf. Therein lies the power of brand and reputation.
High Fixed Costs: In some industries, there are high fixed costs associated with developing and maintaining products or services. This means that a company must make substantial initial investments before seeing any returns. Established firms with deep pockets are better equipped to weather these costs.
Regulatory Barriers: Some markets have regulatory barriers that favor incumbents or limit the entry of new competitors. Licensing requirements, patents, and industry-specific regulations can protect existing players and deter potential challengers.
Investors are often interested in winner-take-all markets because they offer significant profit opportunities, but they also come with higher risks:
Potential for Exceptional Returns: In winner-take-all markets, dominant firms can achieve extraordinary growth and profitability, leading to substantial returns for early investors. For example, investors in companies like Amazon, Google, or Facebook have seen significant gains because they captured the e-commerce, search engine advertising, and social media markets.
Market Monopoly: Dominant players in winner-take-all markets often have a quasi- monopoly, which can lead to stable, long-term revenue streams. This can be attractive to investors seeking steady income. A market monopoly allows a business to generate more profit primarily through its ability to set higher prices due to the lack of competition. With no rivals to challenge them, monopolies can reduce costs associated with marketing and price wars. They benefit from economies of scale, lowering their average costs as production increases.
Monopolies can also create high barriers to entry, protecting their market position and sustaining profitability. Their market control allows for better predictability and strategic planning, while higher profits enable significant investment in research and development. Additionally, monopolies can ensure customer loyalty and consistent revenue by offering unique products or services. However, such dominance often attracts regulatory scrutiny and potential consumer backlash.
Competitive Advantage: Companies that establish themselves as winners in these markets typically have substantial competitive advantages, making them more resilient to economic downturns and market fluctuations.
However, it's crucial to be aware of the risks associated with winner-take-all markets:
High Competition: Entering a winner-take-all market can be highly challenging due to the dominance of existing players. New entrants may find it difficult to gain a foothold.
 
Regulatory Risks: Winner-take-all markets may attract regulatory scrutiny due to concerns about monopolistic behavior, privacy issues, or other market distortions. Regulatory changes can disrupt the competitive landscape and affect investor returns.
Netflix operated in a relatively stable streaming segment for a decade before competition ramped up. If you recall, streaming competition was limited between Netflix’s launch and 2019. The primary options were Netflix, Hulu, and Amazon Prime Video.
These three companies were not lowering prices; other than Netflix, they were not significantly increasing content budgets. The limited competition allowed Netflix to grow to reach 200 million subscribers with little struggle. Netflix regularly added millions of subscribers each quarter while legacy cable and satellite providers sustained losses.
Streaming was more convenient for customers who could watch the content anywhere they could get an internet connection. Taking the bus to school? You can pull out your iPhone and watch an episode of Stranger Things on the ride. Compare that to a cable TV service where you can only watch your content at home in front of the television. It’s no surprise that millions of folks are canceling their cable subscriptions in favor of streaming.
The challenge for the legacy cable companies was that the business was a cash cow. Even though customers are canceling by the millions, the segment generates billions of dollars in revenue and profits. For that reason, companies like Disney and Paramount were slow to launch their own streaming services. They were afraid it would hasten the switch of cable subscribers to streaming.
The hesitation ended at the onset of the pandemic. Stuck at home with fewer entertainment options available, folks enthusiastically demanded streaming services. Since signing up for cable meant having someone come into your home at a time when a potentially deadly virus was in circulation, cable connections were not as attractive.
Disney+, Paramount+, HBO Max, Peacock, Curiosity Stream, Apple TV+, and more all came on the scene with full force in 2020. Admittedly, some of these services may have existed before the outbreak. However, after stay-at-home orders, investments in these services exploded. Content budgets were increased, movies slated for the box office went straight to streaming, advertising campaigns were supercharged, and most offered prices lower than Netflix.
Initially, consumer demand was high enough to absorb all the new entrants with new content. People had plenty of time to watch all the content across several streaming services, so they didn’t mind subscribing to every available option. As economies started reopening, people had more things they could do with their time and money. Further, after being cooped up at home for so long, people wanted to go outside. Demand for streaming content fell. On the flip side, supply kept growing. Corporations have made the commitment to launch streaming services, and there is no turning back from that.
The higher supply and falling demand meant existing customers would be spread over more providers. Netflix reported its first-ever decrease in subscribers. Others accustomed to double-digit millions of subscriber growth quarterly experienced significant slowdowns.
 
Typically, companies in an industry in the early growth stage are more likely to engage in fierce competition. That’s one of the reasons it’s said to be riskier to invest in growth stocks.
With no clear leader, competitive equilibrium, and new customers trying out products, businesses are willing to sacrifice profit margins in the hunt for market share.
As the thinking goes, we can acquire customers before they try our competitors, and if we serve them well, we can retain them as long-term loyal customers. All too often, however, younger companies overestimate the lifetime value of a customer. The error in overcalculation leads them to overspend in order to acquire these customers. If you’re a younger company with only a few years of experience, how can you truly know a customer's lifetime value?
Companies with decades of history can more accurately measure a customer's lifetime value. They’ve observed how their customers have reacted through different business cycles, and the data from the past can be used to make judgments about the future. Still, the riskiness of sacrificing profits to gain market share does not preclude companies in the growth stage from doing just that.
Why would businesses do this? The most likely reason is incentives. CEOs and founders stand to make huge profits if they get it right. Sometimes, management’s compensation gives them massive rewards if the stock price hits a specific benchmark. There are rarely any clawback provisions if the company’s stock price falls after management has been compensated. This can lead to investments in growth that will bring in customers in the short-term, boosting the stock price as the company demonstrates growth and then watching those customers leave to competitors more quickly than estimated in the calculations.
I look for companies that can achieve and sustain a competitive advantage that can protect against competition. One of the experts in the field of competition is Michael Porter. He has developed key concepts and frameworks that provide insights into how businesses can compete effectively in the marketplace. Here are some of his central teachings on competition:
Porter emphasizes the importance of achieving and maintaining a sustainable competitive advantage. He argues that businesses must create a unique value proposition that differentiates them from competitors. Competitive advantage can be achieved through cost leadership (being the low-cost producer), differentiation (offering unique products or services), or focus (targeting a specific market segment). Let’s look at each one of these in more detail.
Cost Leadership:
Value Proposition: The cost leadership strategy is based on becoming the lowest-cost producer in the industry. This means offering products or services at prices lower than those of competitors while maintaining a reasonable level of quality.
Key Features:
Efficient operations and production processes to minimize costs. Economies of scale and scope to reduce per-unit production costs.
 
Cost-effective supply chain management. Streamlined and lean organizational structures.
Examples: Discount retailers like Walmart and low-cost airlines like Southwest Airlines are known for their cost leadership strategies. They provide products and services at lower prices than their competitors. This strategy is the most difficult to implement. Controlling the variables to achieve cost advantage requires the most business skill. That said, it can also provide a long- lasting competitive advantage.
Differentiation:
Value Proposition: Differentiation involves offering unique products or services that customers perceive as superior. This strategy allows a business to command premium prices and build customer loyalty.
Key Features:
Focus on product design, quality, and innovation.
Branding and marketing efforts to create a distinct image and reputation. Customization or personalization to meet specific customer needs.
Superior customer service and support.
Examples: Apple is a prime example of a differentiation strategy. Their products, such as the iPhone and MacBook, are known for their innovative design and user experience, allowing them to command higher prices in the market. This can be the most lucrative strategy.
Combining higher-quality products and an effective branding strategy that convinces consumers you are the best in class creates pricing power, brand loyalty, and higher-than-usual profit margins.
Focus:
Value Proposition: The focus strategy concentrates on a specific market segment, niche, or geographic region. By tailoring products or services to this target audience's unique needs and preferences, a business can develop a solid competitive position.
Key Features:
Deep understanding of the specific needs and preferences of the chosen market segment. Customization or specialization in product offerings.
Building strong relationships within the chosen niche. Avoiding the distractions of serving broader markets.
Examples: Rolex is an example of a focus strategy. They specialize in luxury watches and cater to a niche market of high-end watch enthusiasts, allowing them to command premium
 
prices and maintain exclusivity. The niche strategy has a higher probability of success than the others, although it comes at the expense of a lower upside.
It's important to note that businesses can also pursue hybrid strategies that combine cost leadership and differentiation elements, depending on their industry and competitive landscape. However, to create a unique value proposition, a company must effectively align its chosen strategy with its core competencies and market conditions. It’s not prudent to pick the plan with the best potential if you’re not equipped to execute that strategy.
Ultimately, these unique value propositions aim to provide customers with something they perceive as valuable and distinct, whether it's lower prices, superior product features, or specialized services. This differentiation can help businesses attract and retain customers, increase market share, and achieve long-term success in a competitive marketplace.
How aggressively are rivals competing for market share?
When measuring competition in an industry, you must consider the level and the trend.
Competition could be intense but decreasing or mild but intensifying. Look beyond price to determine the competitive intensity. Price is an excellent place to start, but consider advertising, supply, new products, distribution channels, and talent acquisition.
An increase in advertising intensifies competition in an industry by raising the stakes for market share acquisition. Companies invest more in promoting their products to stand out, which can lead to a competitive advertising "arms race" where firms continually try to outspend each other. This can benefit consumers through better deals and more information, but it also raises the cost of entry for new firms, making it harder for smaller companies to compete. Additionally, increased advertising can enhance brand recognition and loyalty for established players, potentially consolidating their market positions and making it more difficult for new entrants to gain traction. Heightened advertising efforts can sharpen competitive dynamics, benefiting well- funded firms while challenging smaller competitors.
An increase in supply within an industry generally intensifies competition by providing consumers with more choices and putting downward pressure on prices. As more products or services become available, companies must compete more aggressively to attract customers, often leading to price reductions, improved quality, or enhanced features. This increased competition can benefit consumers by offering better value and more options. However, it can also strain profit margins for businesses, particularly those unable to differentiate their offerings or operate efficiently. Additionally, an oversupply can lead to market saturation, forcing weaker competitors out of the market and potentially leading to industry consolidation. Overall, an increase in supply fosters a more competitive environment, driving innovation and efficiency while challenging businesses to maintain profitability.
When new products are introduced into an industry, competition intensifies as companies vie for market share. These new offerings can attract consumers looking for the latest innovations, prompting existing companies to improve their products, lower prices, or enhance marketing efforts to retain customers. The arrival of new products can disrupt established market
 
dynamics, forcing incumbents to adapt quickly. This competition can lead to greater consumer choice and better products overall. However, it can also pressure existing companies to invest more in research and development, marketing, and production to stay competitive. For smaller firms or those unable to innovate rapidly, the introduction of new products can pose significant challenges, potentially leading to market exits or consolidation.
When new distribution channels are introduced in an industry, competition intensifies as companies seek to capitalize on these new avenues to reach consumers. These new channels, such as online platforms, direct-to-consumer models, or emerging retail partnerships, can disrupt traditional distribution methods, compelling businesses to adapt their strategies. Companies may need to enhance their logistics, expand their presence across multiple channels, and innovate their marketing approaches to engage customers effectively.
This increased competition can benefit consumers by providing more convenient and varied purchasing options, often with better pricing and service. However, it also pressures existing businesses to invest in technology and infrastructure to maintain competitiveness. Those able to leverage new distribution channels effectively can gain significant market advantages, while those slow to adapt may struggle to retain their market share. The introduction of new distribution channels fosters a dynamic and competitive market environment, driving efficiency and consumer choice.
When new talent enters an industry, competition intensifies as companies vie to attract and retain the best employees. Fresh talent brings innovative ideas, diverse perspectives, and updated skills, which can significantly enhance a company's competitive edge. To attract top talent, businesses may need to offer more competitive salaries, better benefits, and a positive work environment, which can increase operational costs and drive overall performance improvements.
This influx of talent can lead to increased innovation and productivity within the industry, pushing companies to improve their products, services, and processes. Firms that successfully attract and nurture new talent can gain a strategic advantage, while those that fail may struggle to keep up with industry advancements. Ultimately, the arrival of new talent stimulates a more competitive and dynamic industry, fostering growth and development.


Chapter Summary/Key Takeaways
The chapter discusses the various forms of competition in the business world and their impact on profits. It emphasizes that fierce competition, mainly based on price, can harm profits and lead to extended battles between companies, resulting in shrinking profits. The author notes that businesses often compete in terms of advertising, promotional incentives, and other methods to attract customers.
The chapter provides examples of competition in the food delivery industry, highlighting aggressive promotional offers from companies like DoorDash and Uber Eats that have led to significant financial losses despite revenue growth.
 
The concept of winner-take-all markets is introduced, explaining that a small number of dominant players capture the majority of market share and profits, making it challenging for new entrants. Factors such as network effects, economies of scale, branding, high fixed costs, and regulatory barriers contribute to the emergence of winner-take-all markets.
The impact of competition on streaming services is discussed, citing the increased supply of streaming platforms and the decline in demand as people sought other entertainment options post-pandemic. The author uses Netflix as an example, illustrating how competition led to a decrease in subscribers and a fall in stock prices.
The chapter concludes by discussing the risks and benefits of competition, noting that early-stage growth companies are more likely to engage in fierce competition, often sacrificing short-term profits for market share. The author highlights the importance of sustainable competitive advantage and references Michael Porter's teachings on achieving and maintaining competitive advantage through cost leadership, differentiation, and focus strategies.
Overall, the chapter emphasizes the challenges and risks associated with competition in the business world, underscoring the importance of companies establishing and sustaining a unique value proposition to protect against competition.
 
Chapter Five: Risks
Every investment you make has risks. It can be the risk of losing money. It can also be the risk of inferior return on investment. For instance, if you invest $1,000 in a stock for 30 years and finish with a value of $1,005, you will not be a happy investor. Identifying key risk factors is more helpful when connected to how it could reduce the return on investment or the return of investment. Investors should keep at least eight significant factors in mind as it relates to any investment.
Market risk: This is the risk that the value of an investment will decline due to changes in the broader market. Factors such as economic conditions, political events, or changes in interest rates can all affect market prices. To mitigate market risk, investors can diversify their portfolios by investing in various assets or asset classes. In 2008, the global financial crisis led to a significant decline in stock prices worldwide, resulting in major losses for investors who had heavily invested in the stock market. Additionally, changes in market interest rates influence the valuations investors are willing to pay for stocks. When investors can earn higher interest rates in risk-free assets like government bonds, they prefer to hold more in their portfolios. To make room for those assets, investors sell riskier investments like stocks.
Similarly, investors’ psychology changes sometimes unexpectedly. Sometimes, investors prefer riskier assets and are willing to pay premium prices. The overarching theme during these moments is a fear of missing out. This overall attitude boosts stock prices and valuations to unsustainably high levels. The opposite happens when investors are primarily fearful of losing their money. Risk-averse investors pull their money out of risky assets and place them into safer bond-like investments to protect their capital. During these times, capital protection becomes increasingly more important than capital growth.
The global financial crisis' aftermath was when investors were extremely risk-averse. During these moments in history, great stocks are available at bargain prices. Oppositely, 2021 was a year of hungry, risk-seeking investors. Investors rushed into speculative investments like non-fungible tokens, meme stocks, cryptocurrencies, and electric vehicle stocks. Sadly, these speculative bubbles usually burst, as did this latest occurrence, and many investors lost 95% or more of their investment value.
Credit risk: This is the risk that an issuer of a bond or other debt instrument will default on their payments. Credit risk can be mitigated by investing in bonds with high credit ratings, such as those issued by governments or highly rated corporations. In 2020, the COVID-19 pandemic led to corporate bankruptcies, with several companies defaulting on debt obligations. For example, Hertz Global Holdings, a car rental company, filed for bankruptcy in May 2020, resulting in losses for investors who held Hertz bonds. Since this book is about stocks, I won’t dive deeper into bonds.
Inflation risk: Inflation is the general increase in prices over time, which can erode the value of an investment. To mitigate inflation risk, investors can invest in assets likely to appreciate at a rate higher than inflation, such as stocks or real estate. In the 1970s, inflation in the United States reached double digits, causing the value of investments such as bonds and cash
 
to decline in real terms. Investors who held assets that didn't appreciate at a rate higher than inflation experienced a loss in purchasing power. The critical thing to remember about inflation and investment prices is that the returns offered by the investment need, at the very least, to grow at the inflation rate. Otherwise, investors would be better off spending that money today instead of investing it for the future.
Further, inflation will compress profit margins for all companies that cannot exercise pricing power. After the coronavirus pandemic, governments worldwide stimulated their economies with trillions of dollars in spending packages. Simultaneously, the same geniuses forced businesses to shut their operations or limit productive capacity through safety restrictions. Unsurprisingly, with supply chains constrained and trillions of dollars in extra purchasing power in consumer’s hands, inflation was unleashed, and the prices of nearly everything exploded.
Liquidity risk: This is the risk that an investor may need more time to sell their investment to realize its full value. Illiquid assets like real estate or private equity may be more difficult to sell quickly than liquid investments like stocks or bonds. In 2007-2008, the global financial crisis led to a freeze in the credit markets, making it difficult for investors to sell illiquid assets such as real estate and private equity investments. Stocks are almost always actively traded, so this is not a concern for the main subject of this book. However, I included this risk to inform your decision-making between asset classes. For instance, when deciding between investing in real estate or stocks.
Operational risk: This is the risk that an investment may be impacted by events such as fraud, errors, or other operational failures. Operational risk can be mitigated by investing in well- established companies with solid management and transparent financial reporting. In 2018, the German payments company Wirecard AG admitted to a multi-year accounting fraud, resulting in a significant decline in its stock price and losses for investors who held shares in the company.
The Enron Corporation was an American energy company that, at its peak, was one of the largest and most successful corporations in the United States. However, in the early 2000s, it became embroiled in one of history’s most infamous corporate scandals. Enron's downfall was primarily due to widespread accounting fraud and corporate misconduct. The company used accounting loopholes and special-purpose entities to hide its debt and inflate its profits. Enron's executives engaged in unethical and fraudulent practices to portray the company as financially stable and profitable when, in reality, it was facing significant financial troubles. As the truth unfolded, Enron's stock price plummeted, leading to massive financial losses for investors. In 2001, Enron filed for bankruptcy, marking one of the largest bankruptcies in U.S. history. The scandal not only resulted in the loss of thousands of jobs but also led to the dissolution of the Arthur Andersen accounting firm, which was involved in auditing Enron. The Enron scandal had far- reaching consequences, prompting increased scrutiny of corporate governance, financial reporting, and regulatory practices. It also led to the passage of the Sarbanes-Oxley Act, a comprehensive reform aimed at improving corporate accountability and transparency. Given its destructive power, operational risk is the most important risk to consider for stock market investors.
 
Geopolitical risk: This is the risk that political instability or conflicts between countries could negatively impact investments in those regions. To mitigate geopolitical risk, investors can diversify their portfolios across different regions and economies. In 2014, the annexation of Crimea by Russia and the ensuing conflict in Ukraine led to a decline in the Russian stock market and the value of the Russian ruble, resulting in losses for investors who held Russian assets. Investors should be cognizant of companies with a presence in countries that have demonstrated an unfriendly relationship with business. In recent years, the Chinese government has implemented regulatory crackdowns on various industries, including technology, education, and fintech. Companies such as Alibaba, Tencent, and Didi have faced increased scrutiny, leading to regulatory interventions that impacted their business operations. Ant Group, the financial affiliate of Alibaba, was set to have one of the largest initial public offerings (IPO) in history in 2020. However, Chinese regulators suspended the IPO, citing concerns about Ant Group's corporate governance and regulatory compliance. This move was seen as a significant intervention in the business activities of a major corporation. To this day, investors are hesitant to buy Chinese stocks because of concerns about how its government treats business.
Currency risk: This is the risk that fluctuations in exchange rates can impact the value of an investment denominated in a foreign currency. Foreign subsidiaries are generally required to keep accounting records in the currency of the country in which they are located. To prepare consolidated financial statements, the parent company must translate the foreign currency financial statements of its foreign subsidiaries into its own currency. The net translation adjustment that results from translating individual assets and liabilities at the current exchange rate can be viewed as the net foreign currency translation gain or loss caused by a change in the exchange rate. Those assets and liabilities translated at the current exchange rate are revalued from balance sheet to balance sheet in terms of the parent company’s presentation currency.
These items are said to be exposed to translation adjustment. Currency risk can be mitigated by investing in assets denominated in the investor's home currency or by hedging against currency fluctuations. In 2016, the United Kingdom's vote to leave the European Union led to a decline in the value of the British pound, resulting in losses for investors who held assets denominated in pounds. While currency risk is meaningful, the fluctuations tend to balance over the longer term.
Systematic risk: This is the risk that is inherent to the market as a whole and cannot be diversified away. Systematic risk can be mitigated through long-term investing, diversification, and an investment strategy considering the investor's risk tolerance and goals. In 2020, the COVID-19 pandemic caused a global market crash, with stock prices declining worldwide due to the economic uncertainty caused by the pandemic. This systematic risk impacted all investors, regardless of their portfolio composition. In this scenario, consumers save more of their money in cash-like forms, including actual cash, checking accounts, savings accounts, etc. Likewise, businesses conserve money by reducing discretionary spending, making fewer long-term investments, and taking an altogether cautious approach to capital allocation.
Additionally, systemwide crashes happened in 2007/2008, 2000, 1987, 1929, and more. To mitigate this risk, investors can observe macroeconomic indicators such as unemployment, gross domestic product, inflation, disposable personal income, and others to evaluate the health
 
of a country’s economy. However, no due diligence can completely protect against a systemic crash. I suggest not to invest any money you will need for necessities in the next three years. I recommend having an emergency fund with six months of living expenses.


Identifying the primary sources that could hurt the company’s profitability.
Risks come in various forms, and I wanted to highlight company-specific risks in greater detail. For instance, in 2023, Apple generated 52% of its revenue from the iPhone, not to mention complementary products and services that depend on the customer having an iPhone first (Apple Care, Accessories, etc..). Deriving such a significant share of revenue from a single product is a risk. If a competitor were to grab market share and reduce iPhone sales, it would likely sink the price of Apple stock.
As I will discuss further in the valuation chapter, stocks are primarily valued by discounted cash flow and multiple comparisons. A decrease in iPhone sales will result in Apple’s profits and cash flow following suit. If an investor was willing to pay 10x Apple’s earnings and earnings fell from $4 per share to $2 per share, then Apple’s stock price would fall from $40 per share to $20 per share.
Similarly, Coinbase, a platform that makes money when its users buy and sell cryptocurrency, owes its existence to the relatively new asset class. That opens it to several meaningful risks, including fluctuations in crypto prices. During the early days of the pandemic, you might recall the frenzy in the cryptocurrency industry. Prices of newly created coins were shooting to the stars. Unsurprisingly, Coinbase attracted millions of new customers in the boom times.
When the bubble popped in 2022, the market capitalization of cryptocurrencies fell from
$3 trillion to $1 trillion. People lost their savings after contracting the “fear of missing out.” Sadly, several of my students approached me and told me they took out loans intended to pay for school and used them to buy crypto instead. Later, they found out that some platform or another scammed them.
The price crash and poor publicity that followed the frauds related to cryptocurrencies caused a mass exodus at Coinbase. It lost most of the millions of new customers it gained. Since Coinbase stock is so impacted by what happens to cryptocurrencies, the entire asset class is a risk.
Another risk could be a company’s reliance on labor. Dominos makes affordable pizzas available for delivery and carryout. The risk for Dominos is that this is not software that can be automated. People need to make and deliver these pies. Unfortunately, in the aftermath of the pandemic, there are substantial labor shortages in the U.S. Fewer people are willing to work at the going wages if they have to show up in person.
That’s bad news for Dominos because it either needs to serve fewer customers (i.e., lower revenue) or pay higher wages to attract employees – a lose-lose situation for Dominos. If it pays
 
higher wages to keep workers, then profits decrease. If it closes locations earlier or operates only six days a week, it loses sales, reducing profits. Remember from earlier, investors’ willingness to pay a price for a stock depends on its earnings. The lower the earnings, the lower an investor is willing to pay.
Dominos has grappled with this issue since the economic reopening gained momentum in late 2021 and early 2022. Keep in mind that Dominos thrived during the pandemic. Restaurants were closed to in-person dining, and people had more money in their pockets due to government stimulus and were looking to stay in their homes. Interestingly, demand for Dominos Pizza did not decrease much when economies reopened. Instead, it was this risk to labor that hurt Dominos business.
Who can forget the Bruhaha Meta Platforms encountered in the Summer of 2021 over the lack of enforcement the social media company exercised on its platform? Its users were found posting all kinds of hateful speech, misinformation, and worse. Meta Platforms is a massive company with 3 billion daily active users. That’s an incredible amount of information to monitor and regulate even if you want to.
Meta Platforms is free to use, but the company generates nearly all its revenue from advertising. When large corporations that advertise with Meta started getting backlash for their ads showing up next to hateful speech, they revolted. A boycott ensued, and several large companies refused to advertise on Meta Platforms until the company demonstrated improvement in the areas they demanded.
Investors could have identified the near 100% reliance on advertisers for its revenue as a significant risk of buying Meta Platforms stock. You might think that risk is distributed because each corporation deals with Meta Platforms individually. That would not be completely accurate. Typically, corporations sign with marketing agencies to represent their interests. Media buying agencies specialize in negotiating and purchasing advertising space for their clients. They work with television networks, radio stations, social media platforms, and other media outlets to secure the best possible rates for their clients.
Once the advertising campaign is launched, the marketing agency monitors its effectiveness and makes adjustments to ensure that it achieves the desired results. Since these agencies represent groups of marketers, that risk is more concentrated.
Of course, a chapter on risks can only be completed by discussing debt. Debt can have several negative impacts on a business.
When a business takes on debt, it typically needs to pay interest. The interest expense can become a significant burden, especially if the company has high levels of debt or if interest rates rise. The interest payments reduce the company's profitability and cash flow, potentially limiting its ability to invest in growth opportunities or meet other financial obligations. Risks from long- term debt can be exacerbated depending on the company’s debt. In floating-rate debt, the interest rate is not fixed but instead fluctuates based on a benchmark interest rate, often tied to a reference rate such as LIBOR (London Interbank Offered Rate) or the prime rate. The primary
 
risk with floating-rate debt is the uncertainty of interest rate fluctuations. If market interest rates rise significantly, the borrower's interest expenses will also increase, potentially impacting cash flow. In fixed-rate debt, the interest rate is set at the time of issuance and remains constant throughout the life of the debt. The main advantage of fixed-rate debt is that it provides certainty for both the borrower and the lender. Borrowers know the exact amount of interest they need to pay over the life of the debt, making it easier to plan and budget. However, the downside is that if market interest rates decrease after the debt is issued, the borrower may pay a higher interest rate than prevailing market rates.
High levels of debt increase a company's financial risk. If the business experiences a decline in revenue or faces unexpected expenses, it may struggle to generate enough cash flow to cover its debt payments. In extreme cases, excessive debt can lead to insolvency or bankruptcy. Overall, it reduces the flexibility of the business to adjust to changing consumer demand. Interest expenses must be paid regardless of the state of the company. With such risks, you might ask why any business would raise capital by borrowing. The most likely reason is that it adds operational leverage. I discussed the downside of interest expenses that must be paid when revenue decreases, but there is also an upside. When revenue soars, interest expense is still the same, creating leverage, which increases profitability faster than the revenue increases.
When a company has a large amount of existing debt, it may be more difficult to secure additional financing. When assessing creditworthiness, lenders and investors evaluate a business's debt-to-equity ratio and overall debt burden. A high level of debt can make the company appear riskier, leading to higher borrowing costs or even a denial of credit. Moreover, the cost of borrowing increases exponentially, not linearly. As a company takes on more debt, it becomes a riskier proposition for lenders to extend credit. Therefore, a company that may have borrowed at 4% interest at lower debt totals may have to pay 15% interest if debt levels increase the risk of default.
Debt repayments consume a portion of a company's cash flow, limiting its ability to invest in new projects, research and development, marketing, or hiring. Businesses with high debt levels may be forced to prioritize debt payments over growth initiatives, hindering their competitiveness and expansion opportunities.
Excessive debt can negatively impact a company's reputation and market perception. Investors, customers, and business partners may view high debt levels as a sign of financial instability or poor management. This negative perception can lead to a decline in investor confidence, reduced stock prices, difficulty attracting new customers or partners, and even harm the company's overall brand image.
When businesses take on debt, lenders often impose certain covenants and restrictions. These can include limitations on the company's ability to take on additional debt, make certain financial decisions, or pursue specific business strategies. Failure to comply with these covenants can result in penalties, higher interest rates, or even default.
The management team is one area of business that may not typically be considered a risk. Corporate governance is a critical issue that needs to be addressed. Corporate governance refers
 
to the rules, practices, and processes by which a company is directed and controlled. While effective corporate governance is crucial for a business’s long-term success and sustainability, several risks are associated with inadequate or flawed governance practices. Here are some common risks:
Fraud and unethical behavior: Weak corporate governance can create an environment that fosters fraud, corruption, and unethical behavior. Without proper oversight and controls, executives or employees may engage in financial misreporting, embezzlement, insider trading, or other fraudulent activities. An independent board of directors plays a crucial role in exercising control over management behavior to ensure accountability, transparency, and the protection of shareholder interests. Here are several ways through which an independent board can exercise control:
Appointment and Evaluation of Executives:
The board is typically responsible for appointing and evaluating top executives, including the CEO. The board can set a tone for responsible management behavior by selecting competent and ethical leaders.
Setting Corporate Policies and Guidelines:
The board establishes corporate policies and guidelines that guide management behavior. These policies may cover ethical standards, risk management, financial reporting, and other key aspects of corporate governance.
Approving Strategic Decisions:
Significant strategic decisions, such as mergers, acquisitions, divestitures, and major investments, often require board approval. This ensures that management decisions align with the company’s and its stakeholders' long-term interests.
Monitoring Financial Performance:
The board monitors the company's financial performance, reviewing financial reports and ensuring accurate and transparent financial disclosure. This oversight helps prevent financial misconduct and mismanagement.
Risk Oversight:
The board is responsible for overseeing the company's risk management practices. This includes identifying and assessing risks, implementing risk mitigation strategies, and ensuring that management proactively addresses potential business threats.
Regular Board Meetings and Committees:
Regular board meetings and specialized committees (audit, compensation, nominating, etc.) allow for in-depth discussions and analysis of various aspects of the company's operations. Committees, particularly the audit committee, are critical in scrutinizing financial matters.
Executive Compensation Approval:
 
The board, particularly the compensation committee, approves executive compensation packages. This ensures that executive pay is aligned with the company's performance and shareholder interests.
Whistleblower Mechanisms:
The board establishes mechanisms for whistleblowers to report concerns about unethical behavior or violations of corporate policies. This allows employees and other stakeholders to bring potential issues to the board's attention.
Succession Planning:
The board is involved in succession planning for key executive positions. This proactive approach helps ensure a smooth transition in leadership and minimizes disruptions to the company's operations.
Engaging with Shareholders:
An independent board engages with shareholders, addressing their concerns and seeking input on critical issues. This dialogue helps align the interests of the board and management with those of the shareholders.
By fulfilling these responsibilities, an independent board of directors acts as a crucial check and balance on management behavior, fostering a corporate culture of integrity, accountability, and long-term value creation.
Mismanagement and poor decision-making: Inadequate governance structures can result in poor decision-making processes and ineffective management. Without proper checks and balances, executives may make decisions that are not in the company’s or its shareholders' best interest, leading to financial losses, missed opportunities, or reputational damage.
Conflict of interest: Corporate governance helps ensure that conflicts of interest are adequately managed and transparently disclosed. When conflicts of interest are not appropriately addressed, executives or board members may prioritize personal gain or the interests of related parties over those of the company and its shareholders. Consider the recent acquisition of Twitter by the CEO of Tesla, Elon Musk. The ownership of Twitter presents an interesting conflict of interest at Tesla. The pioneer of the EV industry has yet to spend any meaningful sum on advertising. However, now that Musk owns Twitter, it can be tempting for him to allocate advertising dollars from Tesla to the social media platform he owns. He might also pay premium prices for those advertising services because he stands to benefit. This would present a conflict of interest because Twitter would benefit at the expense of Tesla.
Lack of accountability and transparency: Strong governance promotes accountability and transparency in business operations. Without adequate governance mechanisms, there may be limited disclosure of financial information, inadequate reporting and monitoring, and a lack of oversight of executive actions. This can erode investor trust, increase the cost of capital, and hinder the company's ability to attract investors and partners. In general, anytime a company
 
reduces transparency, it should be a red flag to investors. The direction should be toward increasing transparency as a business grows and its reportable segments grow larger.
Risk management failures: Robust corporate governance is essential for identifying, assessing, and managing risks. When governance structures are weak, inadequate risk management practices may lead to unaddressed or underestimated risks. This can expose the company to financial losses, operational disruptions, legal issues, or reputational harm.
Shareholder dissatisfaction and activism: Ineffective corporate governance can result in shareholder dissatisfaction and activism. Shareholders may voice concerns over executive compensation, board composition, or strategic decisions, leading to proxy battles, lawsuits, or attempts to influence company direction. Such conflicts can distract management, create instability, and disrupt business operations. It’s also important to remember that activist investors seek quick profits. They may highlight specific actions they want management to take that would boost the share price in the near term, with the risk that reduces long-term shareholder value.
Regulatory and legal non-compliance: Weak governance practices increase the risk of regulatory and legal non-compliance. Failure to comply with laws, regulations, or industry standards can lead to fines, penalties, lawsuits, or damage to the company's reputation. Investors can look to a company’s past to observe its history in attracting penalties from regulatory bodies. Banks are notoriously known for paying fines regularly. More recently, technology companies that deal with consumer data are attracting the attention of regulators. In July 2019, Meta, formerly known as Facebook, reached a settlement with the U.S. Federal Trade Commission (FTC) over privacy violations. The settlement included a $5 billion penalty, one of the most significant fines ever imposed on a tech company. The settlement also required Meta to implement enhanced privacy practices and undergo regular assessments of its privacy policies.
Companies should establish robust governance frameworks to mitigate these risks, including independent boards, adequate internal controls, transparent reporting, and strong ethical standards. Regular evaluation and enhancement of governance practices are essential to adapting to changing business environments and maintaining the trust of stakeholders.


Sensitivity Analysis
You can conduct a sensitivity analysis to determine how much a business is exposed to the risk factors mentioned above. It’s a technique used to assess the potential impact of changes in critical variables or assumptions on the outcomes of a business investment or project. It helps businesses understand the sensitivity of their financial projections or decision-making models to different scenarios and variables. By analyzing the potential effects of these changes, companies can gain insights into the risks and uncertainties associated with their investments.
Sensitivity analysis helps identify and quantify the risks associated with an investment or project. By varying input parameters such as sales volume, pricing, costs, or interest rates, businesses can observe the sensitivity of key financial metrics such as net present value (NPV),
 
internal rate of return (IRR), or payback period. This allows them to assess the impact of various risk factors and understand the potential range of outcomes.
Decision-making: Sensitivity analysis provides decision-makers with valuable information to make informed choices. By evaluating different scenarios, they can assess the robustness and resilience of an investment under various conditions. Sensitivity analysis aids in understanding the critical factors that significantly influence the financial performance and success of the investment. This helps decision-makers evaluate alternative strategies, assess trade-offs, and make informed investment decisions.
Mitigating downside risks: Through sensitivity analysis, businesses can identify vulnerable areas where changes in variables significantly negatively impact project outcomes. This enables them to focus on risk mitigation measures and develop contingency plans. By understanding the risks associated with an investment, businesses can take proactive steps to minimize potential losses, adjust strategies, or allocate resources accordingly.
Optimizing resource allocation: Sensitivity analysis allows businesses to prioritize resource allocation based on potential risks and rewards. By understanding the sensitivity of different investment options or projects, companies can allocate resources to those with favorable risk-reward profiles and higher potential returns. This helps optimize capital allocation and ensure that resources are allocated to resilient projects with the highest likelihood of success.
Enhanced communication with stakeholders: Sensitivity analysis facilitates effective communication with stakeholders, including investors, lenders, or board members. It provides a clear understanding of the risks and uncertainties associated with an investment, enabling stakeholders to make informed decisions. By transparently presenting the sensitivity analysis results, businesses can build confidence, demonstrate thorough analysis, and improve communication about their investments' potential outcomes and risks.
Let's consider an example of a company planning to undertake a long-term investment project, such as building a new manufacturing facility. The company is considering financing the project through equity and debt. The company can perform a sensitivity analysis to assess the exposure to interest rate risk.
Here's how the sensitivity analysis could be conducted:
Identify the key variables: In this case, the key variable is the interest rate. The company would analyze how changes in interest rates can impact the financial viability of the investment.
Define the range of interest rate scenarios: The company would determine a range of possible interest rate scenarios, considering both favorable and unfavorable changes. For example, they could analyze three scenarios: a decrease of 1%, the current interest rate, and an increase of 1%.
Assess the impact on financial metrics: The company would evaluate how changes in interest rates affect various financial metrics of the project. These metrics may include net
 
present value (NPV), internal rate of return (IRR), cash flows, or debt service coverage ratio (DSCR).
Calculate the outcomes under different interest rate scenarios: The company would recalculate the financial metrics based on the new interest rates using the identified scenarios. This would adjust cash flows, discount rates, and debt service costs accordingly.
Analyze the results: The company would examine the sensitivity analysis results to understand the exposure to interest rate risk. They would compare the outcomes of different scenarios to assess how changes in interest rates impact the financial viability of the investment. For example, a higher interest rate scenario might reduce the NPV, while a lower interest rate scenario could increase it.
Mitigate risks and make informed decisions: Based on the sensitivity analysis results, the company can take steps to mitigate interest rate risks. They may explore options such as renegotiating the debt terms, considering interest rate hedging strategies, adjusting the financing mix, or seeking alternative funding sources.


Chapter Summary/Key Takeaways
Investing inherently involves potential financial losses or lower-than-expected returns. Recognizing and managing different types of risks is essential for achieving financial success. Key risks include:
Market Risk:
The potential for investment losses due to changes in the broader economy, political events, or interest rate shifts.
Diversifying across asset classes (e.g., stocks, bonds, real estate) can help mitigate market
risk.
Example: The 2008 global financial crisis caused significant drops in stock prices,
resulting in substantial losses for investors.
Investor Psychology: Emotions like the fear of missing out (FOMO) or fear of losses can influence investment decisions, leading to speculative bubbles (e.g., the 2021 NFT and cryptocurrency boom and subsequent crash).
Credit Risk:
The risk is that a bond issuer may fail to make payments, leading to losses for bondholders.
High-rated bonds, such as government or well-established corporate bonds, generally carry lower credit risk.
 
Example: In 2020, Hertz Global Holdings’ bankruptcy caused bondholders to lose money because the company could not meet its debt obligations.
Inflation Risk:
The risk is that inflation will erode the purchasing power of investments over time.
Assets like stocks, real estate, or inflation-protected bonds typically appreciate faster than inflation, helping protect against this risk.
Example: In the 1970s, high inflation significantly reduced the real value of investments like bonds and cash, diminishing their purchasing power.
Conclusion:
Investors should consider market, credit, and inflation risks when making investment decisions. Using strategies like diversification and choosing inflation-resistant assets can help.










Chapter Six: Valuation

This chapter on valuation will be the longest in the book. Understandably, almost any stock can be an excellent investment at a cheap price. Similarly, even the most outstanding business can make a poor investment if you pay a steep enough price. Therefore, valuation is the most critical investment aspect, and I will give it the time it deserves.
Notably, the valuation is completely different from the price. I often use the example of how supermarkets sell soda. You can buy soda in 12-ounce cans, 20-ounce bottles, and 2-liter bottles. It would not surprise you that the 12-ounce can is often priced the lowest. That does not necessarily make it the best value.
Let’s say the 12-ounce can is priced at $0.50. Let’s also assume that the 20-ounce bottle is priced at $0.60. The 12-ounce can will be priced the lowest, but the 20-ounce bottle would be the best value. That’s because when you buy the 12-ounce can, you pay $.042 per ounce. For the 20-ounce bottle, you’re paying $0.03. In other words, you’re getting more soda percent when you buy the 20-ounce bottle. The price per ounce is lower, which is the critical value factor.
It's a similar consideration when investing in stocks. Sure, one stock might sell at a lower price than another, but that doesn’t mean it’s a better value. We need to look at the inside to
 
understand which stock has the best value. We need to find what we are getting for our price. Remember, stocks represent ownership in a business. Buying a share of Apple stock means you own a small piece of the Apple corporation.
Typically, I want profits, cash flow, and asset growth out of ownership of a business.
Therefore, I look at the underlying company’s net profits, free cash flow, and assets when looking to find value. I am trying to answer how much earnings per share I am getting for purchasing this stock. How much free cash flow per share? If I have to pay a price to earnings of 30 for one company, that company is relatively more expensive than another I can buy at a price to earnings of 10.
There are instances where I prefer to buy the stock selling at a higher valuation, but only because I am getting more value for the price. For instance, maybe this stock is selling at a higher price to earnings, but there is a high likelihood that this company’s earnings will grow by 40% each year for the next five years. How would you know that? It might be evident in the company’s financial statements. That’s what financial analysis can uncover.
For example, a company like Boeing knows with a relatively high probability what its sales and earnings will look like for at least two years. The company signs contracts for the sale of its planes in advance and secures pricing with its suppliers years in advance so it can determine what its sales, expenses, and profits will look like several years into the future. It discloses this information to investors, who can use it to determine what valuation they are willing to pay for a share of Boeing stock.
Similarly, there are situations when you know a company’s earnings will fall for the next several quarters or years. In those instances, you are paying a price to earnings for a stock today, and a few years later, you are left with a company with a much smaller earnings total. That should cause you to lower the price you’re willing to pay to buy the stock because you know you will get less value in the future.
To summarize the first part of this chapter, the market price is only the numerator in determining value in the stock market. The other part of the story is the denominator, which can be earnings per share, free cash flow, sales, and many other desirable business characteristics you can use. A stock only becomes a good value if you like the price per unit(s).
Earnings per share
Earnings per share is the most comprehensive figure to use as the denominator. I emphasize this figure when deciding if a stock is priced favorably. EPS incorporates sales and all the company’s expenses to generate those sales. It incorporates a proportional share of fixed expenses like rent, depreciation, and amortization of intangible assets.
Additionally, it accounts for any stock splits or stock buybacks management implements.
A stock split is a corporate action in which a company increases the number of outstanding shares by dividing existing shares into multiple ones. For example, in a 2-for-1 stock split, a shareholder who owns 100 shares before the split would own 200 shares after the split, but the total value of their holdings would remain the same.
 
Stock splits are usually done to make shares more affordable and increase market liquidity. By lowering the price per share, more investors may be able to purchase the stock, potentially increasing demand and trading volume. This can also help to improve the stock's visibility and attract new investors.
Stock splits sometimes create enthusiasm among unsophisticated investors. After a stock split, the price per share of a stock is lowered, leading these investors to think they are getting a better deal (remember the section on price versus value). Management is not faultless about capitalizing on this belief. They could use it as a relatively easy way to boost their share price, even if it is a temporary boost.
Stock splits do not affect a company's overall market capitalization, earnings, or financial performance. However, they can affect the stock price and the company's price-to-earnings ratio, as the earnings per share will be divided among more shares.
Stock splits are typically announced by companies that have seen a significant increase in their share price. They are usually implemented by issuing new shares to existing shareholders proportionally. Stock splits can also be reversed through a reverse stock split, in which the number of outstanding shares is reduced, resulting in a higher price per share.
A stock buyback, also known as a share repurchase, is a financial strategy that allows a company to buy back its shares from the market. When a company buys back its shares, it reduces the number of outstanding shares, which can increase the value of the remaining shares.
A company can initiate stock buybacks for various reasons. One common reason is to return excess cash to shareholders. By buying back shares, the company reduces the number of shares outstanding, increasing earnings per share (EPS) and return on equity (ROE). This can make the company's stock more attractive to investors and potentially increase its share price.
Another reason for a stock buyback is to signal to the market that the company believes its stock is undervalued. By buying back shares, the company effectively invests in itself, which can boost investor confidence and increase demand for the stock. After all, a company management team has the most information about its prospects. If they are buying shares, it sends a message that they think the shares are undervalued. Since they are using cash to repurchase shares, this is an expensive signal to fake.
Stock buybacks can be executed through open market purchases, where the company buys shares on the open market like any other investor, or through a tender offer, where the company offers to buy back shares from shareholders at a premium price.
That said, EPS is exposed to manipulations in the short run. One such manipulation is when the management of a company makes sales on credit to make profits look better than they organically would be.
Consider this: would you buy a three-year-old iPhone for $2,000? Most of you reading this book are savvy individuals; otherwise, you would not likely have money to invest in the market. I don’t suspect you would answer yes to that question. But what if I modified that offer?
 
What If I told you that the price would stay the same, but you would only have to pay me if your income in the current year increases by 10x what you made the previous year? Indeed, that would have changed the answer to yes for many people.
If my income increases by 10x, something few of us are expecting, I would not mind paying a higher price for this iPhone. However, in the most likely scenario, my income will not increase by 10x, and I will have this iPhone for free. I know that’s an extreme example, but many businesses boost sales and profits in a less extreme but similar manner. When sales and profits look sluggish for a quarter, management sometimes offers better credit terms to buyers to increase purchases.


Is the stock valued cheaply, moderately, or expensively?
I will discuss four valuation methods to determine whether the stock's price is expensive or cheap. The first is historical valuation, the second is relative valuation, the third is the dividend discount model, and the fourth is the free cash flow model. Financial professionals use each of these in various forms today. The most comprehensive analysis uses all these to get several answers on valuation.
Historical valuation looks at a stock’s price compared to how much it sold for in the past. To answer if the stock is cheap according to historical valuations, you compare the current price to earnings (P/E) ratio with the P/E ratio of the last ten or more years (if the data are available). In addition to doing this exercise with the P/E ratio, you add the Price to Free Cash Flow (P/FCF), Price to Sales (P/S), and some enterprise value metrics.
If the stock sells at a P/E and P/FCF at its lowest levels in fifteen years, it is cheap according to its history. Likewise, the stock is expensive if it is the priciest it has been according to those metrics. Ideally, you want to target stocks trading at the lower end of their historical valuations.
Similar to historical valuation is relative valuation. In this exercise, you take the same financial metrics as mentioned above and compare them to competitors. Instead of looking at P/E and asking if it’s the lowest it’s been, you ask if it’s lower than competitors. Looking at five social media stocks, one trades at a P/E lower than the others. Your work doesn’t end there.
Then, you have to dig deeper to answer if that lower valuation is justified. Sometimes, stocks have earned a lower valuation.
For instance, comparing Home Depot to Lowe’s, investors will realize Home Depot has traded at a more expensive valuation than Lowe’s between 2012 and 2022. Looking at Home Depot’s operating profit margin (OPM) at the same time mentioned above, you will notice that Home Depot’s OPM has increased. Meanwhile, the same metric at Lowe’s improved, but less so than at Home Depot. Admittedly, they are both impressive regarding the growth in operating profit margin, but Home Depot proves superior. A consistently better operating profit margin is an excellent reason to pay a higher price for one stock over another.
 
The final method I will discuss to determine if the stock is a good bargain is discounted cash flow models. Specifically, I will highlight the dividend discount and free cash flow models. The dividend discount model (DDM) is a method used to estimate the intrinsic value of a company's stock by discounting the present value of its future dividends. The basic idea behind the DDM is that the value of a company's stock is equal to the sum of all future dividends, discounted back to their present value.


The formula for the DDM is as follows:


V₀ = D₁ / (r - g)


Where:


V₀ is the current fair value of the stock
D₁ is the expected dividend payment for the next year
r is the required rate of return or discount rate for the stock g is the expected growth rate of the dividend
	2021	2022	2023
Dividends	3	3.12	3.2448
			
			
D1	3		
Required Return	0.09		
Growth Rate	0.04		
			
			
Stock Price	60		


In other words, the DDM assumes that a company's stock price is based on the present value of all future expected dividend payments, which are assumed to grow at a constant rate. The required return (r) is typically derived from the capital asset pricing model to determine its cost of equity. It is generally based on historical growth rates, industry trends, and management projections.
The DDM is a popular tool used by investors to evaluate the fundamental value of a stock, but it is important to note that it has some limitations. For example, it assumes that dividends will be paid out regularly and at a constant rate, which may not always be accurate in
 
practice. Additionally, it may only be appropriate for companies that pay dividends or have consistent dividend payment patterns. When a company does not pay dividends, the traditional DDM cannot be used. In such cases, there are several ways to modify the DDM to estimate the value of the stock.
One approach is to estimate the company’s likely future dividend payments. This can be done by analyzing its financial statements, cash flow projections, and other relevant data. The future dividend payments can then be used as inputs to the DDM formula to estimate the stock's intrinsic value.

2021	2022	2023	2024	2025	2026
0	0	0	3	3	3
In the figure above, dividends are zero for the next three years. Then, in the fourth year, it starts paying a $3.00 dividend.
Another approach is to use alternative cash flows instead of dividends. For example, if the company is expected to generate significant cash flows from operations or to have substantial capital expenditures, these cash flows can be discounted using a variation of the DDM formula that includes cash flows instead of dividends.
A third approach is comparing the stock with similar stocks that pay dividends. This can be done by analyzing other companies’ financial performance and valuation metrics in the same industry or sector. The dividend yields and payout ratios of these companies can be used as a benchmark to estimate the potential future dividend payments of the target company.
As you may have noticed, the formula for valuing a stock using dividends has several assumptions. The required rate of return on a stock can be derived from the capital asset pricing model (CAPM). The CAPM is a financial model that aims to determine the expected return on an investment based on its risk. It was first proposed by William Sharpe in the 1960s and has become a widely used tool in finance.
The CAPM is based on the following formula:
r = rf + β * (rm - rf) where:
•	r is the expected return on the investment
•	Rf is the risk-free rate of return, which is the return on an investment that has zero risk, such as the return on U.S. Treasury bills.
•	β is the beta coefficient, which measures the systematic risk of the investment relative to the market. A beta of 1 indicates that the investment has the same level of risk as the market, while a beta greater than 1 indicates that the investment is riskier than the market. A beta less than 1 indicates that the investment is less risky than the market.
 
•	Rm is the expected market return, usually represented by a stock market index such as the S&P 500. The term (rm—rf) is known as the market risk premium, which is estimated to be between 4% and 6%.
The CAPM assumes that investors are rational and risk-averse and require a higher return for taking on additional risk. The model uses the beta coefficient to adjust the expected return on the market for the additional risk associated with the investment. The risk-free rate is added to the adjusted market return to arrive at the expected return on the investment.
The CAPM has been criticized for its assumptions and limitations, such as the assumption of a single-factor model and the difficulty of accurately estimating beta coefficients. However, it remains a useful tool for estimating the expected return on an investment and comparing it to other investment opportunities.
To counter some of the downsides of the CAPM, investors can conduct a scenario analysis. I can best explain this process through examples. For instance, let’s say your initial calculation for the required return using the CAPM gives you a figure of 6%. In that instance, I would compute the value of the stock using the DDM with the 6% figure as the required return, but I would also compute additional valuations using 5%, 4%, 7%, and 8% as the required return.
The additional calculations do not require much extra work if you’re using a spreadsheet like Microsoft Excel. However, the information that it provides is vital. Instead of just one intrinsic value for the stock under analysis, you get several. Going further into this example, let’s say the four values you get from your calculations are $45, $50, $35, and $30. Notice that the higher required returns will generate lower valuation estimates. Finally, you can compare your outcomes with the stock’s market price. If the market price is $59, you can comfortably say that the stock is overvalued according to your calculations. That’s because, in every scenario you considered, the intrinsic value was below the market price.
You can feel better about your conclusion because you used several estimates. This should account for some of the uncertainty involved in making decisions based on estimates and assumptions.
Similar to the dividend discount model is the free cash flow valuation model. The free cash flow (FCF) valuation model estimates the intrinsic value of a company's equity by forecasting its future cash flows available to equity holders. Free cash flow is the cash generated by a company's operations that is available to be distributed to debt holders and equity holders after the company has made all the necessary capital expenditures to maintain or grow its operations.
To use the FCF valuation model, you need to estimate the company's future free cash flows and determine the appropriate discount rate to apply to those cash flows to arrive at a present value. The discount rate is usually the company's weighted average cost of capital (WACC), which represents the cost of financing the company's operations through a combination of debt and equity.
The formula for the FCF valuation model is as follows:
 
FCF = Operating Cash Flow - Capital Expenditures

V  	FCFt
 

Value of the Company's Operations =

Vop,0
 

 
t  1 1 WACCt
	FCF1
WACC gL
 
Horizon Value of the Company =
Here, t represents the number of years into the future that you want to forecast the company's FCF. To calculate the FCF, you subtract the capital expenditures from the operating cash flow. Then, you calculate the present value of the FCF by dividing it by the sum of 1 and the WACC raised to the nth power.


in billions of dollars	2024	2025e	2026e	2027e	2028e	2029e
Free Cash Flows	$47	$69	$101	$149	$218	$321
PV of cash flows	$573	$62	$81	$106	$140	$184
						
PV of Horizon value	$2,844				Horizon value	$4,966
Value of operations	$3,417					

Summing up those individual cash flows will bring you the present value of the cash flow in the forecasted timeline. Remember, the company's value is the discounted free cash flow from now until infinity. That said, forecasting cash flow from now until eternity will be tedious. What I do instead is forecast cash flows to some horizon period. In the example above, I have forecasted six years of cash flow. That’s because I can accumulate the present value of all the expected cash flows between year five and infinity.
The formula to find the horizon value of the business at any point in time = The FCF expected one year ahead / The Weighted Average Cost of Capital (WACC) – The Long Run Growth Rate. Remember, this long-run growth rate must be lower than the WACC for this formula to work. That’s why I forecasted cash flows to year six when I wanted the horizon value for year five.

Value of operations	$3,416,738,065,130
Non-op-assets	$34,800,000,000
Debt	$11,000,000,000
# of shares	24,800,000,000
Value of Equity	$3,440,438,065,130
 

Intrinsic value per share	$138.73

Since this model only considers a company’s value from operations, we must also consider its non-operating assets. To the calculations above, we would add short-term investments, marketable securities, and ownership of any non-controlling interest in another company. These values are typically reported on the balance sheet. We also need to deduct any long-term debt and preferred stock. Again, we can find these values in the balance sheet.
Using this model, you can estimate the intrinsic value of a company's equity based on its ability to generate free cash flows in the future. If the estimated value exceeds the current market price, the stock may be undervalued and a good investment opportunity. Conversely, if the estimated value is lower than the current market price, the stock may be overvalued and not a good investment opportunity.
Since this model only considers a company’s value from operations, we must also consider its non-operating assets. To the total calculated above, we would add short-term investments, other marketable securities, and ownership of non-controlling interest in another company. These values are typically reported on the balance sheet. We also need to deduct any long-term debt and preferred stock. Again, we can find these values on the balance sheet.
Notice a few differences between the FCF model and the DDM. First, you are using free cash flows compared to dividends on the numerator. On the denominator, you are using the WACC compared to the required rate of return. One key difference between these two models is how they account for the cost of capital. The FCF model uses the Weighted Average Cost of Capital (WACC), which reflects the cost of all of a company's capital (both debt and equity). In contrast, the DDM uses the required rate of return, which is the minimum rate of return that investors expect to earn on their investment in the company's stock.
The primary reason for using the WACC in the FCF model is that it considers the company's entire capital structure and the cost of each component of capital, whereas the required rate of return in the DDM only reflects the cost of equity capital. Additionally, free cash flows are available to both lenders and equity investors, whereas dividends are only paid to shareholders, not lenders.
At this point, let’s consider the WACC in more detail. The weighted average cost of capital (WACC) is a calculation that considers the proportional cost of each type of capital a company uses to finance its operations. The three main components of a company's capital structure are debt, preferred stock, and common equity.
The WACC formula is:
WACC = (E/V x Re) + (D/V x Rd x (1 - T))
Where:
•	E = market value of the company's equity
 
•	V = total market value of the company's debt and equity
•	D = market value of the company's debt
•	Re = cost of equity
•	Rd = cost of debt
•	T = corporate tax rate
To calculate the WACC, you must first determine the market value of the company's equity and debt. The market value of equity is simply the current stock price multiplied by the number of shares outstanding. The market value of debt is the sum of all outstanding debt, including both short-term and long-term obligations.
Next, you need to determine the cost of each component of the company's capital structure. The cost of equity is typically estimated using the capital asset pricing model (CAPM) or other models considering the risk associated with investing in the company's stock. The cost of debt is typically calculated as the yield to maturity on the company's outstanding debt.
Once you have calculated the cost of equity and debt, you can use the formula above to calculate the WACC. The resulting number represents the average cost of capital that the company must pay its investors to finance its operations, considering the relative weights of each component of its capital structure.
Similar to what we did in the DDM, we can increase the robustness of our calculations by using additional results close to our initial outcome. If your computations give you a WACC of 8%, it would be worthwhile to compute the stock’s value using additional WACCs of 7%, 6%, 9%, and 10%. As I mentioned earlier, the information gained from the incremental work is worth the effort.
Digging even deeper, investors can do a reverse DCF. A reverse discounted cash flow (DCF) valuation model is a method used to calculate the implied growth rate of a company's future cash flows, based on its current market price. Unlike a traditional DCF model that starts with future cash flows and discounts them to arrive at a present value, a reverse DCF model works backward from the current market price to calculate the growth rate that would justify the stock's current valuation.
To use a reverse DCF model, you need to have the current market price of the stock, as well as a forecast of the company's future cash flows. You would then calculate the implied growth rate that would be necessary for the company to generate enough cash flow to justify its current market price.
The formula for a reverse DCF model is as follows:
Current Market Price = Future Cash Flows / (Discount Rate - Implied Growth Rate)
 
Here, the Discount Rate refers to the required rate of return for investors, which can be estimated using the Capital Asset Pricing Model (CAPM). The Implied Growth Rate is the rate at which the company's cash flows are expected to grow.
By solving for the Implied Growth Rate, you can get an estimate of the growth rate that the market is currently expecting from the company and compare this to your estimates of the company's future growth prospects. If the implied growth rate is higher than your estimates, the stock may be overvalued, while if it is lower than your estimates, the stock may be undervalued.
I’ve spent some time on the required rate of return and the WACC, the denominators in the valuation models. Now, I want to move on to forecasting the dividends in the DDM or looking at the valuation model's numerator. There are several methods for forecasting a company's dividends.
1.	Historical dividend growth: This method involves examining the company's historical dividend growth rate and assuming that it will continue at the same rate. It can be simple and straightforward, but it may not be accurate if there are significant changes in the company's business or the broader economic environment.
2.	Dividend payout ratio: This method involves looking at the company's historical dividend payout ratio and assuming it will remain the same. This assumes the company will continue to have a similar dividend policy and earnings growth rate. Still, it may not consider changes in its capital needs or other factors that could affect the payout ratio. The dividend payout ratio measures the percentage of a company's earnings paid to shareholders as dividends. A sustainable dividend payout ratio is one that the company can maintain over the long term without jeopardizing its financial health.
To determine if a company's dividend payout ratio is sustainable, several factors must be considered: Historical dividend payout ratio: Look at the company's past dividend payout ratios and see if they have been consistently paying dividends and if the ratio has been stable. Industry standards: Compare the company's dividend payout ratio to the industry average. A company with a higher ratio than its peers may be paying out too much and could be at risk of cutting its dividend.
Earnings growth: Look at the company's earnings growth rate. If the company's earnings are increasing at a healthy rate, it should be able to sustain its dividend payout ratio. Free cash flow: Check the company's free cash flow to see if it generates enough cash to cover its dividend payments. If the dividend payments exceed the company's free cash flow, it may not be sustainable.
Debt levels: Look at the company's debt levels to determine if it has enough financial flexibility to continue paying its dividend. If a company has a high debt load, it may not be able to sustain its dividend payments in the long term. Overall, it is essential to look at a company's financial health and consider both its historical performance and prospects when assessing the sustainability of its dividend payout ratio.
 
3.	Analyst forecasts: Analysts who cover a particular company may also provide estimates for the company's future dividends based on their analysis of its financial statements, industry trends, and other factors. These forecasts can be helpful as a starting point, but they may vary widely depending on the analyst's assumptions and methodology.
Forecasting a company's dividends involves a combination of historical analysis, forward-looking assumptions, and careful analysis of the company's financial statements and industry trends. All the methods can be used to derive various estimates, resulting in a more comprehensive study.





Chapter Summary/Key Takeaways


The chapter summary on valuation delves into its pivotal role in investment decisions, underscoring the necessity of discerning between price and value. A key principle introduced is that any stock can be a good investment at the right (low) price, while even the best company can turn into a poor investment if its stock price becomes excessively high. This distinction between price and value is crucial for informed decision-making.


Valuation refers to determining a stock's or investment’s worth, which may not always align with its market price. Market prices fluctuate due to a variety of factors, such as supply and demand, sentiment, and short-term speculation, but true value is derived from underlying financial fundamentals, such as earnings, growth potential, and the overall health of the company. The idea is that price is what you pay, but value is what you get. Understanding this difference allows investors to avoid overpaying for assets.


An analogy used in the chapter involves soda packaging to illustrate the concept of value: a consumer might find a 12-ounce soda can cheaper than a 20-ounce bottle, but the 20-ounce bottle offers more soda per dollar spent. Similarly, a stock might have a low price with investments, but if its growth potential or profitability is limited, it may not offer much value.
Conversely, a higher-priced stock could provide better value if its long-term prospects are strong. This comparison stresses that just because something has a lower price doesn’t mean it’s a better deal in terms of value.


The chapter explains that understanding valuation helps investors make better-informed choices. It allows them to assess whether a stock is undervalued, overvalued, or fairly priced,
 
which can directly influence their return on investment over time. Valuation methods, such as discounted cash flow (DCF) analysis or price-to-earnings (P/E) ratios, help investors quantify value and avoid the common trap of chasing high-flying stocks without regard to their actual worth.
Ultimately, the chapter underscores that valuation is the cornerstone of wise investing. By focusing on an asset’s intrinsic value rather than getting distracted by market prices, investors can position themselves for long-term success.
 
The Algorithm
Concluding the chapter on valuation might deceive you into thinking that it is the end-all-be-all for decision-making. That’s not the case for me. I use valuation in conjunction with the other five factors. Sometimes, you will be fortunate and find a company that excels in every factor.

For instance, if I find a company that demonstrates an excellent customer value proposition, generates profit margins in the top 10% of all companies, operates in a multi-trillion-dollar industry that’s growing, where competition is decreasing from an already low point, risks are most prevalent in non-significant parts of its business, and the valuation calculations signal it is undervalued, the stock is an instant buy. The next question becomes how much I should buy.

Factor Weightings	
Valuation	40
Risks	15
Unit Economics	15
Customer Value	10
Total market size	10
Competition	10


Let me zoom out a little bit. Even though I have discussed six factors I consider when evaluating stocks, they are not all equal. The valuation factor should be given greater weight. After all, the greatest business makes a poor investment if you pay too much. I give the valuation factor forty percent of the weighting in decision-making.

In the chart above, I present the weighting of each of the six factors. When evaluating a business, I give it a score on each factor. My rule of thumb is that a stock is a buy if it scores above 80 on all factors combined. I trust my bias if I am on the fence about a stock. After over 10,000 hours of study and 15,000 hours of practice, I feel cautiously confident in trusting my gut.

There you have it. Those are my six factors for evaluating stocks. They have worked well for me, and I hope they will work well for you. Remember, the output is only as good as the input. So, take your time researching before parting ways with precious money. It is not guaranteed that you will make money using this process. However, if you master the steps outlined in this book, you can be reasonably confident your investment results will be positive.
 
 
 


# --------------------------
# Page Config
# --------------------------
st.set_page_config(page_title="Stock Analysis App", page_icon="📈", layout="wide")

# --------------------------
# Chatbot Utilities (Hugging Face Inference API - free endpoint)
# --------------------------
HF_CHAT_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"  # good free-chat model via HF Inference API
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_CHAT_MODEL}"
HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")  # optional; public/free tier often works without token

SYSTEM_PROMPT = (
    "You are a helpful support assistant for a Streamlit stock analysis app. "
    "Answer user questions about using the app, understanding metrics (P/E, P/B, ROE), "
    "data sources, and general app troubleshooting. Keep answers concise."
)

def hf_chat_completion(messages: list[dict], max_new_tokens: int = 256, temperature: float = 0.2) -> str:
    headers = {"Accept": "application/json"}
    if HF_API_TOKEN:
        headers["Authorization"] = f"Bearer {HF_API_TOKEN}"
    payload = {
        "inputs": {
            "past_user_inputs": [m["content"] for m in messages if m["role"] == "user"],
            "generated_responses": [m["content"] for m in messages if m["role"] == "assistant"],
            "text": messages[-1]["content"] if messages else "Hello",
        },
        "parameters": {"max_new_tokens": max_new_tokens, "temperature": temperature}
    }
    try:
        r = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()
        # HF conversation models may return dict with 'generated_text' or a list
        if isinstance(data, dict) and "generated_text" in data:
            return data["generated_text"].strip()
        if isinstance(data, list) and len(data) and isinstance(data[0], dict):
            # some endpoints return [{'generated_text': '...'}]
            gt = data[0].get("generated_text") or data[0].get("summary_text")
            if gt:
                return gt.strip()
        # Fallback if text generation style
        if isinstance(data, dict) and "conversation" in data:
            conv = data["conversation"]
            if isinstance(conv, dict) and "generated_responses" in conv and conv["generated_responses"]:
                return conv["generated_responses"][-1].strip()
        return "Sorry, I couldn't generate a response right now. Please try again."
    except Exception as e:
        return f"Chat service error: {e}"

# --------------------------
# Helper Functions
# --------------------------

def fetch_sp500_tickers():
    """Fetch S&P 500 tickers from Wikipedia"""
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        tables = pd.read_html(url)
        sp500_table = tables[0]
        tickers = sp500_table['Symbol'].tolist()
        # Clean tickers (replace dots with dashes for Yahoo Finance compatibility)
        tickers = [ticker.replace('.', '-') for ticker in tickers]
        return tickers
    except Exception as e:
        st.error(f"Error fetching S&P 500 tickers: {e}")
        return []

def fetch_stock_data(ticker):
    """Fetch stock price and financial data using yfinance"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        data = {
            'Ticker': ticker,
            'Name': info.get('longName', 'N/A'),
            'Current_Price': info.get('currentPrice', np.nan),
            'PE_Ratio': info.get('trailingPE', np.nan),
            'PB_Ratio': info.get('priceToBook', np.nan),
            'PS_Ratio': info.get('priceToSalesTrailing12Months', np.nan),
            'Dividend_Yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
            'ROE': info.get('returnOnEquity', np.nan) * 100 if info.get('returnOnEquity') else np.nan,
            'Profit_Margin': info.get('profitMargins', np.nan) * 100 if info.get('profitMargins') else np.nan,
            'Revenue_Growth': info.get('revenueGrowth', np.nan) * 100 if info.get('revenueGrowth') else np.nan,
            'EPS': info.get('trailingEps', np.nan),
            'Beta': info.get('beta', np.nan),
            'Market_Cap': info.get('marketCap', np.nan),
            'Sector': info.get('sector', 'N/A')
        }
        return data
    except Exception:
        return None

def calculate_valuation_score(row):
    """Calculate a composite valuation score based on multiple factors"""
    score = 0
    weight_total = 0
    # Lower P/E is better
    if pd.notna(row['PE_Ratio']) and row['PE_Ratio'] > 0:
        pe_score = max(0, 100 - (row['PE_Ratio'] - 10) * 2)
        score += pe_score * 0.25
        weight_total += 0.25
    # Lower P/B is better
    if pd.notna(row['PB_Ratio']) and row['PB_Ratio'] > 0:
        pb_score = max(0, 100 - (row['PB_Ratio'] - 1) * 20)
        score += pb_score * 0.20
        weight_total += 0.20
    # Lower P/S is better
    if pd.notna(row['PS_Ratio']) and row['PS_Ratio'] > 0:
        ps_score = max(0, 100 - (row['PS_Ratio'] - 1) * 15)
        score += ps_score * 0.15
        weight_total += 0.15
    # Higher ROE is better
    if pd.notna(row['ROE']) and row['ROE'] > 0:
        roe_score = min(100, row['ROE'] * 5)
        score += roe_score * 0.20
        weight_total += 0.20
    # Higher Profit Margin is better
    if pd.notna(row['Profit_Margin']) and row['Profit_Margin'] > 0:
        margin_score = min(100, row['Profit_Margin'] * 5)
        score += margin_score * 0.10
        weight_total += 0.10
    # Higher Dividend Yield is better (bonus)
    if pd.notna(row['Dividend_Yield']) and row['Dividend_Yield'] > 0:
        div_score = min(100, row['Dividend_Yield'] * 20)
        score += div_score * 0.10
        weight_total += 0.10
    if weight_total > 0:
        return score / weight_total
    return 0

# --------------------------
# Main App
# --------------------------

st.title("📈 Global Stock & ETF Analysis App")
st.markdown("### Powered by yfinance - Live Market Data")

# Sidebar
st.sidebar.header("Analysis Options")
analysis_mode = st.sidebar.radio(
    "Select Analysis Mode:",
    ["S&P 500 Top Undervalued Stocks", "Custom Ticker Analysis"]
)

# Chatbot UI in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("💬 Support Chatbot")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
user_msg = st.sidebar.text_input("Ask a question about using this app:", placeholder="e.g., What does P/E mean?")
col_chat1, col_chat2 = st.sidebar.columns([3,1])
with col_chat1:
    ask = st.button("Ask")
with col_chat2:
    clear = st.button("Clear")
if clear:
    st.session_state.chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
if ask and user_msg.strip():
    st.session_state.chat_history.append({"role": "user", "content": user_msg.strip()})
    # build alternating messages excluding system for HF conversation format
    convo = [m for m in st.session_state.chat_history if m["role"] != "system"]
    reply = hf_chat_completion(convo)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

# Render recent messages (last 6 shown)
for m in st.session_state.chat_history[-6:]:
    if m["role"] == "user":
        st.sidebar.markdown(f"🧑‍💻 **You:** {m['content']}")
    elif m["role"] == "assistant":
        st.sidebar.markdown(f"🤖 **Bot:** {m['content']}")

if analysis_mode == "S&P 500 Top Undervalued Stocks":
    st.header("🔍 S&P 500 Undervalued Stock Analysis")
    st.markdown("""
    This analysis:
    1. **Fetches S&P 500 tickers** from Wikipedia
    2. **Uses yfinance** to get live price and financial data
    3. **Runs valuation scoring** based on P/E, P/B, P/S, ROE, Profit Margin, and Dividend Yield
    4. **Shows the top 10 undervalued stocks** with the best scores
    """)
    if st.button("🚀 Run S&P 500 Analysis", type="primary"):
        with st.spinner("Fetching S&P 500 tickers from Wikipedia..."):
            sp500_tickers = fetch_sp500_tickers()
        if sp500_tickers:
            st.success(f"✅ Fetched {len(sp500_tickers)} S&P 500 tickers")
            with st.spinner("Analyzing stocks... This may take a few minutes..."):
                results = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                for idx, ticker in enumerate(sp500_tickers):
                    status_text.text(f"Analyzing {ticker} ({idx+1}/{len(sp500_tickers)})")
                    data = fetch_stock_data(ticker)
                    if data:
                        results.append(data)
                    progress_bar.progress((idx + 1) / len(sp500_tickers))
                status_text.empty()
                progress_bar.empty()
                if results:
                    df = pd.DataFrame(results)
                    df['Valuation_Score'] = df.apply(calculate_valuation_score, axis=1)
                    df_valid = df[df['Valuation_Score'] > 0].copy()
                    df_sorted = df_valid.sort_values('Valuation_Score', ascending=False)
                    top_10 = df_sorted.head(10)
                    st.success(f"✅ Analysis complete! Found {len(df_valid)} stocks with sufficient data.")
                    st.header("🏆 Top 10 Undervalued Stocks")
                    display_cols = ['Ticker', 'Name', 'Sector', 'Current_Price', 'PE_Ratio', 'PB_Ratio', 'ROE', 'Profit_Margin', 'Dividend_Yield', 'Valuation_Score']
                    st.dataframe(
                        top_10[display_cols].style.format({
                            'Current_Price': '${:.2f}',
                            'PE_Ratio': '{:.2f}',
                            'PB_Ratio': '{:.2f}',
                            'ROE': '{:.2f}%','Profit_Margin': '{:.2f}%','Dividend_Yield': '{:.2f}%','Valuation_Score': '{:.2f}'
                        }).background_gradient(subset=['Valuation_Score'], cmap='RdYlGn'),
                        use_container_width=True
                    )
                    st.subheader("📊 Valuation Score Comparison")
                    fig, ax = plt.subplots(figsize=(12, 6))
                    ax.barh(top_10['Ticker'], top_10['Valuation_Score'], color='steelblue')
                    ax.set_xlabel('Valuation Score')
                    ax.set_title('Top 10 Undervalued S&P 500 Stocks')
                    ax.invert_yaxis()
                    st.pyplot(fig)
                    csv = df_sorted.to_csv(index=False)
                    st.download_button(label="📥 Download Full Analysis (CSV)", data=csv, file_name="sp500_valuation_analysis.csv", mime="text/csv")
                else:
                    st.error("No data retrieved. Please try again.")
        else:
            st.error("Failed to fetch S&P 500 tickers.")
elif analysis_mode == "Custom Ticker Analysis":
    st.header("🔎 Custom Ticker Analysis")
    ticker_input = st.text_input("Enter ticker symbol (e.g., AAPL, MSFT, TSLA):", "AAPL")
    if st.button("Analyze Ticker", type="primary"):
        if ticker_input:
            with st.spinner(f"Fetching data for {ticker_input}..."):
                data = fetch_stock_data(ticker_input.upper())
            if data:
                st.success(f"✅ Data retrieved for {ticker_input.upper()}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Company", data['Name'])
                    st.metric("Current Price", f"${data['Current_Price']:.2f}" if pd.notna(data['Current_Price']) else "N/A")
                    st.metric("Sector", data['Sector'])
                with col2:
                    st.metric("P/E Ratio", f"{data['PE_Ratio']:.2f}" if pd.notna(data['PE_Ratio']) else "N/A")
                    st.metric("P/B Ratio", f"{data['PB_Ratio']:.2f}" if pd.notna(data['PB_Ratio']) else "N/A")
                    st.metric("Beta", f"{data['Beta']:.2f}" if pd.notna(data['Beta']) else "N/A")
                with col3:
                    st.metric("ROE", f"{data['ROE']:.2f}%" if pd.notna(data['ROE']) else "N/A")
                    st.metric("Profit Margin", f"{data['Profit_Margin']:.2f}%" if pd.notna(data['Profit_Margin']) else "N/A")
                    st.metric("Dividend Yield", f"{data['Dividend_Yield']:.2f}%" if pd.notna(data['Dividend_Yield']) else "N/A")
                df_temp = pd.DataFrame([data])
                valuation_score = calculate_valuation_score(df_temp.iloc[0])
                st.subheader("Valuation Score")
                st.progress(valuation_score / 100)
                st.write(f"**Score: {valuation_score:.2f} / 100**")
                ticker_obj = yf.Ticker(ticker_input.upper())
                hist = ticker_obj.history(period="6mo")
                if not hist.empty:
                    st.subheader("📈 Price History (Last 6 Months)")
                    fig, ax = plt.subplots(figsize=(12, 6))
                    ax.plot(hist.index, hist['Close'], linewidth=2, color='steelblue')
                    ax.set_xlabel('Date'); ax.set_ylabel('Price ($)')
                    ax.set_title(f'{ticker_input.upper()} Price History (6 Months)')
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
            else:
                st.error(f"Could not fetch data for {ticker_input.upper()}. Please check the ticker symbol.")
        else:
            st.warning("Please enter a ticker symbol.")

st.sidebar.markdown("---")
st.sidebar.info("📊 **Data Source:** Yahoo Finance via yfinance\n\n⚠️ **Disclaimer:** This tool is for educational purposes only. Not financial advice.")
