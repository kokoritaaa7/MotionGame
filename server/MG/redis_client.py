class RedisRanker:    
    """레디스를 이용한 랭커"""
    def __init__(self, conn_redis, key, is_ranker_reset=True):
        """
          :param conn_redis:Redis<ConnectionPool<Connection>>: 레디스연결객체
          :param key:str: 랭커를 저장할 Redis Key
          :param is_ranker_reset:bool: 랭커를 초기화하고 시작할지 여부
        """        
        self.conn_redis = conn_redis
        self.key  = key
        if is_ranker_reset is True:
            self.conn_redis.delete(self.key)

    def getScore(self, str_member):
        """
          멤버 점수를 조회한다
          :param str_member:str: 조회할 멤버
          :return score:float: 멤버 점수
        """
        return int(self.conn_redis.zscore(name=self.key, value=str_member) or 0)
    
    def getRank(self, str_member):
        """
          멤버 랭킹을 조회한다
          :param str_member:str: 조회할 멤버
          :return num_rank:int: 멤버 랭킹(1위 1, 2위 2 리턴), -1 이면 랭킹 정보 없음
        """
        rank = self.conn_redis.zrevrank(name=self.key, value=str_member)

        return rank + 1 if rank is not None else -1
    
    def getTops(self, return_count=20):
        """
          상위 랭킹 몇 개에 대해 리턴한다
          :param return_count:int: 리턴할 개수
          :return tops:list: 상위에 위치한 멤버 리스트
        """        
        return self.conn_redis.zrevrangebyscore(name=self.key, min="-inf", max="+inf", start=0, num=return_count)
    
    def setScore(self, str_member, score):
        """
        멤버 점수를 저장한다.
        :param str_member:str: 저장할 멤버 이름
        :param score:int: 저장할 점수
        :return flag:int: 0은 해당 이름이 이미 있을 때, 1은 해당 이름이 없을 때 (저장은 완료되고 리턴값만 다를뿐)
        """
        return int(self.conn_redis.zadd(name=self.key, mapping={str_member: score}))
    
    def findRank(self, str_member, length=19):
      """
      멤버 랭킹부터 20개 조회
      :param str_member:str : 조회할 멤버
      :param length:int: 조회할 길이
      :return rank_list:list: 해당 멤버부터 아래로 length개 만큼 조회한 결과 리스트
      """
      rank = self.getRank(str_member)
      if rank < 0:
          return None
      
      rank_list = self.conn_redis.zrange(name=self.key, start=rank-1, end=rank+length, desc=True, withscores=True)
      result = []
      for idx, (name,score) in enumerate(rank_list):
          result.append([rank+idx, name, int(score)])
      
      return result

