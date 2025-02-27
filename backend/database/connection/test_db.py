import json
from random import choice
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.models.models import Discount, Price, Purchase, Reward, Setting, User, UserDiscounts
from backend.database.models.models import UCCode


async def init_db(session):
    try:
        db_exist = (await session.execute(select(UCCode))).scalars().all()
        if db_exist:
            await session.close()
            return
        
        setting = Setting(store_is_on=True)
        
        uc_codes_values = {60: [10, 1], 325: [200, 4], 660: [300, 5], 1800: [2000, 8], 3850: [5500, 10], 8100: [10000, 20]}
        
        uc_codes = []
        rewards = []
        for key, value in uc_codes_values.items():
            price = Price(
                price=value[0], 
                point=value[1],
                uc_amount=key
            )
            session.add(price)
        for uc_code in list(uc_codes_values.keys())[:3]:
            rewards.append(
                Reward(
                    reward_type="uc_code",
                    uc_amount=uc_code
                )
            )
        
        discounts = {100: 1000, 200: 2000, 300: 3000, 500: 5000}
        for key, value in discounts.items():
            rewards.append(
                Reward(
                    reward_type="discount", 
                    discount=Discount(
                        value=key, 
                        min_payment_value=value
                    )
                )
            )
        
        session.add_all(rewards)
        await session.commit()
        session.add_all(uc_codes)
        session.add(setting)
        await session.commit()
        await session.close()
    except Exception as e:
        print(e)
    finally:
        await session.close()


async def init_admins(session: AsyncSession):
    try:
        zeus_nis = await session.get(User, 5718861071)
        if not zeus_nis:
            zeus_nis = User(tg_id=5718861071, username="zeucNIS", is_admin=True)
            session.add(zeus_nis)
        zeus_uc = await session.get(User, 494055871)
        if not zeus_uc:
            zeus_uc = User(tg_id=494055871, username="zeucUC", is_admin=True)
            session.add(zeus_uc)
        mago = await session.get(User, 5163648472)
        if not mago:
            mago = User(tg_id=5163648472, username="magoxdd", is_admin=True)
            session.add(mago)
        await session.commit()
    except Exception as e:
        pass
    finally:
        await session.close()